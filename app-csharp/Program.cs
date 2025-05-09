using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;
using Azure.Messaging.ServiceBus;
using Azure.Identity;

class Program
{
    private static string FullyQualifiedNamespace = "soam-sb-namespace.servicebus.windows.net";
    private static string TopicName = "soam-topic";
    private static string SubscriptionName = "soam-subscription";
    private static string QueueName = "soam-queue";

    static async Task Main(string[] args)
    {
        if (args.Length != 3)
        {
            Console.WriteLine("Usage: dotnet run <messages_per_thread> <message_prefix> <mode(write/read/both)>");
            return;
        }

        int messagesPerThread = int.Parse(args[0]);
        string messagePrefix = args[1];
        string mode = args[2].ToLower();

        Console.WriteLine($"Using Service Bus: fully_qualified_namespace={FullyQualifiedNamespace}, topic_name={TopicName}, subscription_name={SubscriptionName}, queue_name={QueueName}");
        ServiceBusClient client = new ServiceBusClient(FullyQualifiedNamespace, new DefaultAzureCredential());

        try
        {
            if(mode=="write" || mode=="both")
            {
                await RunWriteScalingTest(client, messagesPerThread, messagePrefix);
            }
            if(mode=="read" || mode=="both")
            {
                await RunReadScalingTest(client);
            }
        }
        finally
        {
            await client.DisposeAsync();
        }
    }

    // New: Run write scaling test over different thread counts and print a table
    private static async Task RunWriteScalingTest(ServiceBusClient client, int messagesPerThread, string messagePrefix)
    {
        int[] threadCounts = new int[] { 1, 2, 4, 8, 16, 32, 64, 128, 256};
        List<(int threads, double throughput)> results = new List<(int, double)>();

        foreach (int threads in threadCounts)
        {
            Stopwatch sw = Stopwatch.StartNew();
            List<Task> writerTasks = new List<Task>();
            for (int i = 0; i < threads; i++)
            {
                // Invoke the lambda so it returns a Task
                writerTasks.Add(Task.Run(async () =>
                {
                    ServiceBusSender sender = client.CreateSender(TopicName);
                    List<ServiceBusMessage> batch = new List<ServiceBusMessage>();
                    for (int j = 0; j < messagesPerThread; j++)
                    {
                        string body = $"{messagePrefix} T{threads} #{j}";
                        batch.Add(new ServiceBusMessage(body));
                    }
                    await sender.SendMessagesAsync(batch);
                }));
            }
            await Task.WhenAll(writerTasks);
            sw.Stop();
            double throughput = (threads * messagesPerThread) / sw.Elapsed.TotalSeconds;
            results.Add((threads, throughput));
            Console.WriteLine($"Write test with {threads} threads: {(threads * messagesPerThread)} messages in {sw.Elapsed.TotalSeconds:F2}s -> {throughput:F0} msg/s");
            await Task.Delay(2000); // short delay between tests
        }
        // Print results table
        Console.WriteLine("\nWrite Scaling Results:");
        Console.WriteLine("------------------------------");
        Console.WriteLine("| Threads | Throughput (msg/s) |");
        Console.WriteLine("------------------------------");
        foreach (var res in results)
        {
            Console.WriteLine($"| {res.threads,7} | {res.throughput,18:F0} |");
        }
        Console.WriteLine("------------------------------\n");
    }

    // New: Run read scaling test over different thread counts and print a table
    private static async Task RunReadScalingTest(ServiceBusClient client)
    {
        int[] threadCounts = new int[] { 1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096 };
        List<(int threads, double throughput)> results = new List<(int, double)>();

        foreach (int threads in threadCounts)
        {
            List<string> receivedMessages = new List<string>();
            ServiceBusProcessor processor = client.CreateProcessor(QueueName, new ServiceBusProcessorOptions
            {
                ReceiveMode = ServiceBusReceiveMode.PeekLock,
                MaxConcurrentCalls = threads,
                PrefetchCount = 2000
            });

            processor.ProcessMessageAsync += async args =>
            {
                string body = Encoding.UTF8.GetString(args.Message.Body);
                receivedMessages.Add(body);
                await args.CompleteMessageAsync(args.Message);
            };

            processor.ProcessErrorAsync += async args =>
            {
                Console.WriteLine($"Error: {args.Exception.Message}");
                await Task.CompletedTask;
            };

            Stopwatch sw = Stopwatch.StartNew();
            await processor.StartProcessingAsync();
            Console.WriteLine($"Read test with {threads} threads: processing messages for 10 seconds...");
            await Task.Delay(10000); // fixed processing time
            await processor.StopProcessingAsync();
            sw.Stop();

            double throughput = (receivedMessages.Count) / sw.Elapsed.TotalSeconds;
            results.Add((threads, throughput));
            Console.WriteLine($"Read test with {threads} threads: {receivedMessages.Count} messages in {sw.Elapsed.TotalSeconds:F2}s -> {throughput:F0} msg/s");
            await Task.Delay(20000); // short delay between tests
        }
        // Print results table
        Console.WriteLine("\nRead Scaling Results:");
        Console.WriteLine("------------------------------");
        Console.WriteLine("| Threads | Throughput (msg/s) |");
        Console.WriteLine("------------------------------");
        foreach (var res in results)
        {
            Console.WriteLine($"| {res.threads,7} | {res.throughput,18:F0} |");
        }
        Console.WriteLine("------------------------------\n");
    }

    private static async Task WriteMessages(ServiceBusClient client, int threads, int messagesPerThread, string messagePrefix)
    {
        async Task Writer(int idx)
        {
            ServiceBusSender sender = client.CreateSender(TopicName);
            List<ServiceBusMessage> batch = new List<ServiceBusMessage>();

            for (int i = 0; i < messagesPerThread; i++)
            {
                string body = $"{messagePrefix} T{idx} #{i}";
                batch.Add(new ServiceBusMessage(body));
            }

            await sender.SendMessagesAsync(batch);
        }

        Stopwatch sw = Stopwatch.StartNew();
        List<Task> writerTasks = new List<Task>();
        for (int i = 0; i < threads; i++)
        {
            writerTasks.Add(Writer(i));
        }
        await Task.WhenAll(writerTasks);
        sw.Stop();
        Console.WriteLine($"Sent {threads * messagesPerThread} messages in {sw.Elapsed.TotalSeconds:F2}s -> {threads * messagesPerThread / sw.Elapsed.TotalSeconds:F0} msg/s");

        Console.WriteLine("Sleeping for 5 seconds to let messages settle...");
        await Task.Delay(5000);
    }

    private static async Task ReadMessages(ServiceBusClient client, int threads)
    {
        List<string> receivedMessages = new List<string>();
        ServiceBusProcessor processor = client.CreateProcessor(QueueName, new ServiceBusProcessorOptions
        {
            ReceiveMode = ServiceBusReceiveMode.PeekLock,
            MaxConcurrentCalls = 4096,
            PrefetchCount = 4000
        });

        processor.ProcessMessageAsync += async args =>
        {
            string body = Encoding.UTF8.GetString(args.Message.Body);
            receivedMessages.Add(body);
            await args.CompleteMessageAsync(args.Message);
        };

        processor.ProcessErrorAsync += async args =>
        {
            Console.WriteLine($"Error: {args.Exception.Message}");
            await Task.CompletedTask;
        };

        Stopwatch sw = Stopwatch.StartNew();
        await processor.StartProcessingAsync();

        Console.WriteLine("Processing messages...");
        await Task.Delay(10000); // Adjust delay based on expected processing time
        await processor.StopProcessingAsync();
        sw.Stop();

        Console.WriteLine($"Read {receivedMessages.Count} messages in {sw.Elapsed.TotalSeconds:F2}s -> {receivedMessages.Count / sw.Elapsed.TotalSeconds:F0} msg/s");
    }
}
