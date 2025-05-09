# Message Passing Performance Project: Technical Report 4

## Table of Contents

- [Message Passing Performance Project: Technical Report 4](#message-passing-performance-project-technical-report-4)
  - [Table of Contents](#table-of-contents)
  - [Code Repository](#code-repository)
  - [System Architecture](#system-architecture)
    - [What’s New in This Phase?](#whats-new-in-this-phase)
  - [Implementation Details](#implementation-details)
    - [What’s New in This Phase?](#whats-new-in-this-phase-1)
  - [Experimental Results](#experimental-results)
    - [Write Test](#write-test)
    - [Read Test](#read-test)
    - [Results](#results)
    - [Read Performance After Idling](#read-performance-after-idling)
  - [Conclusions](#conclusions)
  - [References](#references)

---

## Code Repository

The code repository for the project is available at [message-passing-azure](https://github.com/vladtf/message-passing-azure).


## System Architecture

The system architecture was introduced in the previous report. It consists of the following components:

1. **Azure Service Bus Namespace** – The message broker.
2. **Service Bus Topic** – Handles published messages.
3. **Service Bus Queue** – Messages are forwarded here.
4. **Python Application** – Sends & receives messages.
5. **Terraform** – Infrastructure as code tool for deployment.

Following is the architecture diagram for the simple message passing system:

<img src="assets/architecture_diagram.png" alt="Architecture Diagram" width="90%" style="border: 1px solid #ccc; padding: 10px; margin: 5px;"/>

### What’s New in This Phase?

There were no major architectural changes from the previous phase. The key updates are:

* Migration of the Python application to **C#**.
* Upgrade of Azure Service Bus to the **Premium** tier.

These modifications significantly improved system performance.


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

Additionally, the application was rewritten in **C#**, using `ServiceBusProcessor` for improved concurrent message processing.

### What’s New in This Phase?

The most impactful configuration updates include:

* **`PrefetchCount`** – Enables the receiver to prefetch a specified number of messages, reducing round-trips.
* **`MaxConcurrentCalls`** – Allows multiple messages to be processed in parallel.

Example configuration:

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

As Azure Service Bus is a managed service, performance was evaluated using the following metrics:

1. **Write Throughput** – Messages sent per second.
2. **Read Throughput** – Messages read per second.
3. **Resource Utilization** – CPU and memory usage of the Service Bus.

### Write Test

* Conducted tests with varying numbers of writer threads (from 1 to 256), each sending a fixed number of messages.
* Measured elapsed time to compute throughput (messages/second).
* Purpose: Assess how system scales with parallel producers and uncover batching or network bottlenecks.

### Read Test

* Tested scaling with different numbers of concurrent reader threads (from 1 up to 4096), using `ServiceBusProcessor`.
* For a fixed duration (e.g., 10 seconds), recorded successfully processed messages.
* Purpose: Understand consumer-side scaling behavior.

### Results

**Service Bus resource utilization during tests:**

The memory utilization of the Service Bus reached 90% during the tests, while CPU utilization was around 80%. This indicates that the Service Bus was able to handle the load without any issues. The following graphs show the resource utilization during the tests:

<img src="assets/resource_utilization.png" alt="Resource Utilization" width="90%" style="border: 1px solid #ccc; padding: 10px; margin: 5px;"/>

**Write Scaling Results:**

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


<img src="assets/write_scaling.png" alt="Write Scaling" width="90%" style="border: 1px solid #ccc; padding: 10px; margin: 5px;"/>

**Read Scaling Results:**

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

<img src="assets/read_scaling.png" alt="Read Scaling" width="90%" style="border: 1px solid #ccc; padding: 10px; margin: 5px;"/>


### Read Performance After Idling

After idling for 30 seconds, the read performance showed a noticeable improvement, likely due to reduced throttling by the Service Bus. The results are summarized below:

| Threads | Throughput (msg/s) |
| ------- | ------------------ |
| 4096    | 5821               |

## Conclusions

The project is currently implemented and working, I've tested the performance of the system and the results are promising. During the performance test, I was able to achieve a throughput of 16,000 messages per second for writing and 5,800 messages per second for reading. What I have learned from this project is that the performance of the system can be significantly improved by using message batching and other techniques. Another important finding is that the Service Bus throttles the number of reads, which can be a bottleneck in the system. It's also important to note that the performance of the system can be improved by using the Premium tier of Service Bus, which allows for better scalability and performance.

Some of the improvements that can be made to the system are:
- Implement sharding of messages to reach a linearly scaling of the system[1]. This can be achieved by using multiple queues and topics, which can be used to distribute the load across multiple partitions.
- Azure Service Bus supports multiple protocols, including AMQP, HTTP, and WebSockets. It might be interesting to test the performance of the system using different protocols and see how they affect the performance of the system.


## References

- [Best Practices for performance improvements using Service Bus Messaging](https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-performance-improvements?tabs=net-standard-sdk-2)