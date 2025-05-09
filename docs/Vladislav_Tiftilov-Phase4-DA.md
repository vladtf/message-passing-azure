# Message Passing Performance Project: Technical Report 2

## Table of Contents

- [Message Passing Performance Project: Technical Report 2](#message-passing-performance-project-technical-report-2)
  - [Table of Contents](#table-of-contents)
  - [Code Repository](#code-repository)
  - [System Architecture](#system-architecture)
    - [What is new in this phase?](#what-is-new-in-this-phase)
  - [Implementation Details](#implementation-details)
    - [What is new in this phase?](#what-is-new-in-this-phase-1)
  - [Experimental Results](#experimental-results)
    - [Write Test](#write-test)
    - [Read Test](#read-test)
    - [Results](#results)
  - [Conclusions](#conclusions)
  - [References](#references)

---

## Code Repository

The code repository for the project is available at [message-passing-azure](https://github.com/vladtf/message-passing-azure).


## System Architecture

The architecture of the system was described in the previous report. The architecture consists of the following components:
1. **Azure Service Bus Namespace** – The message broker.
2. **Service Bus Topic** – Handles published messages.
3. **Service Bus Queue** – Messages are forwarded here.
4. **Python Application** – Sends & receives messages.
5. **Terraform** – Infrastructure as code tool for deployment.

Following is the architecture diagram for the simple message passing system:

<img src="assets/architecture_diagram.png" alt="Architecture Diagram" width="90%" style="border: 1px solid #ccc; padding: 10px; margin: 5px;"/>

### What is new in this phase?

The architecture did not change significantly since the previous report. The only change is that the Python application was migrated to C# and that Service Bus was upgraded to Premium tier. These changes significantly improved the performance of the system.


## Implementation Details

The implementation is described in the previous report. The only changes is that the Terraform code was updated to use the Premium tier of Service Bus:

```terraform
resource "azurerm_servicebus_namespace" "soam" {
  name                = "soam-sb-namespace"
  location            = azurerm_resource_group.soam.location
  resource_group_name = azurerm_resource_group.soam.name
  sku                 = "Premium" # Changed to Premium tier
  capacity = 4
  premium_messaging_partitions = 4
}
```

Another change was the migration of the Python application to C#. Usage of the `ServiceBusProcessor` improved the performance of the system by allowing multiple messages to be processed concurrently.

### What is new in this phase?

The most significant configuration change was the `PrefetchCount` and `MaxConcurrentCalls` parameters. The `PrefetchCount` parameter allows the receiver to prefetch a specified number of messages from the queue, which can improve performance by reducing the number of round trips to the server. The `MaxConcurrentCalls` parameter allows multiple messages to be processed concurrently, which can also improve performance.
The following code snippet shows how to configure the `ServiceBusProcessor`:

```csharp
var processorOptions = new ServiceBusProcessorOptions
{
    ReceiveMode = ServiceBusReceiveMode.PeekLock,
    MaxConcurrentCalls = 4096,
    PrefetchCount = 4000
};
var processor = client.CreateProcessor(queueName, processorOptions);
```

Another improvement was achieved by batching messages. The `ServiceBusSender` class allows you to send messages in batches, which can improve performance by reducing the number of round trips to the server. The following code snippet shows how to send messages in batches:

```csharp
var sender = client.CreateSender(queueName);
var batch = new List<ServiceBusMessage>();
for (int i = 0; i < messagesPerThread; i++)
{
    var message = new ServiceBusMessage($"Message {i}");
    batch.Add(message);
}
await sender.SendMessagesAsync(batch);
```


## Experimental Results

Because Service Bus is a fully managed service, the performance of the system was evaluated using the following metrics:
1. **Write Throughput** – The number of messages sent per second.
2. **Read Throughput** – The number of messages read per second.
3. **Resource Utilization** – The CPU and memory usage of the Service Bus.

### Write Test
- I ran a series of tests where different numbers of writer threads (from 1 up to 256) each sent a fixed number of messages.
- For each test, I measured the elapsed time to send all messages, then calculated the throughput as the total messages sent divided by the elapsed time (messages per second).
- This test reveals how well the system scales with an increasing number of parallel producers and identifies any bottlenecks in batching and network transmission.

### Read Test
- The read test was implemented by varying the number of concurrently processing threads (from 1 up to 4096) using the ServiceBusProcessor.
- Over a fixed duration (e.g., 10 seconds), I measured the total number of messages successfully received and processed.
- The throughput was then computed as the number of messages processed per second.
- This test highlights the scaling behavior of the message consumer.

### Results

Following shows the resource utilization of the Service Bus during the performance test:

<img src="assets/resource_utilization.png" alt="Resource Utilization" width="90%" style="border: 1px solid #ccc; padding: 10px; margin: 5px;"/>

Write Scaling Results:
| Threads | Throughput (msg/s) |
| ------- | ------------------ |
| 1       | 1736               |
| 2       | 10063              |
| 4       | 12599              |
| 8       | 14846              |
| 16      | 15419              |
| 32      | 16637              |
| 64      | 16932              |
| 128     | 16579              |
| 256     | 16593              |
| 512     | 16728              |


Read Scaling Results:
| Threads | Throughput (msg/s) |
| ------- | ------------------ |
| 1       | 12                 |
| 2       | 26                 |
| 4       | 53                 |
| 8       | 99                 |
| 16      | 199                |
| 32      | 421                |
| 64      | 817                |
| 128     | 1610               |
| 256     | 2602               |
| 512     | 2805               |
| 1024    | 2642               |
| 2048    | 2575               |
| 4096    | 2280               |


One of the most interesting observations was that the read performance decreased during the performance test. The conclusion is that the Service Bus throttles the number of reads. The following table shows the read performance after idling for 30 seconds:

| Threads | Throughput (msg/s) |
| ------- | ------------------ |
|    4096 |               5821 |

## Conclusions

The project is currently implemented and working, I've tested the performance of the system and the results are promising. During the performance test, I was able to achieve a throughput of 16,000 messages per second for writing and 5,800 messages per second for reading. What I have learned from this project is that the performance of the system can be significantly improved by using message batching and other techniques. Another important finding is that the Service Bus throttles the number of reads, which can be a bottleneck in the system. It's also important to note that the performance of the system can be improved by using the Premium tier of Service Bus, which allows for better scalability and performance.

Some of the improvements that can be made to the system are:
- Implement sharding of messages to reach a linearly scaling of the system[1]. This can be achieved by using multiple queues and topics, which can be used to distribute the load across multiple partitions.
- Azure Service Bus supports multiple protocols, including AMQP, HTTP, and WebSockets. It might be interesting to test the performance of the system using different protocols and see how they affect the performance of the system.


## References

- [Best Practices for performance improvements using Service Bus Messaging](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-performance-improvements?tabs=net-standard-sdk-2)