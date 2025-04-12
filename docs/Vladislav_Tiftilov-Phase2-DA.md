# Message Passing Performance Project: Technical Report 2

## Table of Contents

- [Message Passing Performance Project: Technical Report 2](#message-passing-performance-project-technical-report-2)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Description of Existing Solutions](#2-description-of-existing-solutions)
    - [2.1 Apache Kafka](#21-apache-kafka)
      - [Problem Addressed](#problem-addressed)
      - [Core Principles \& Algorithms](#core-principles--algorithms)
      - [Architecture](#architecture)
    - [2.2 RabbitMQ](#22-rabbitmq)
      - [Problem Addressed](#problem-addressed-1)
      - [Core Principles \& Algorithms](#core-principles--algorithms-1)
      - [Architecture](#architecture-1)
    - [2.3 AWS SNS + SQS](#23-aws-sns--sqs)
      - [Problem Addressed](#problem-addressed-2)
      - [Core Principles \& Algorithms](#core-principles--algorithms-2)
      - [Architecture](#architecture-2)
    - [2.4 MQTT with Mosquitto](#24-mqtt-with-mosquitto)
      - [Problem Addressed](#problem-addressed-3)
      - [Core Principles \& Algorithms](#core-principles--algorithms-3)
      - [Architecture](#architecture-3)
  - [3. Strengths and Weaknesses Analysis](#3-strengths-and-weaknesses-analysis)
  - [4. Conclusion](#4-conclusion)
  - [References](#references)


---

## 1. Introduction

This project focuses on **message passing performance** in distributed systems, specifically using **Azure Service Bus**. The rationale for this choice is to explore the capabilities of **Azure Service Bus** as a message broker in a distributed architecture. I want to integrate this solution to my dissertation project, which focuses on building a Smart City middleware platform. Specifically, I will be using **Azure Service Bus** to facilitate communication between sensors and the middleware platform, eventually to handle the communication between the components of the platform itself. The goal is to evaluate the performance of message passing in a distributed system and provide an optimized architecture for large-scale applications.

The project will simulate a **publish-subscribe** messaging pattern, where messages are sent from a sensor (publisher) to a middleware platform (subscriber) via **Azure Service Bus**. To match the **SNS** + **SQS** architecture, the project will utilize **Service Bus Topics** as entry points for messages and **Service Bus Queues** to store messages for processing.


---

## 2. Description of Existing Solutions

### 2.1 Apache Kafka

#### Problem Addressed

Apache Kafka solves the problem of high-throughput, low-latency message streaming in distributed systems. It is used in real-time analytics, log aggregation, and event sourcing. This design allows for the system to handle up to **millions of messages per second** with low latency, making it suitable for high-throughput applications[1].

#### Core Principles & Algorithms

Kafka uses a **publish-subscribe** pattern with a **distributed commit log**. Key principles include:

- **Partitioning**: Topics are divided into partitions for parallelism. This allows the system to scale horizontally.
- **Replication and Leader Election**: Each partition has a leader and multiple followers. This ensures fault tolerance and high availability.
- **Consumer Offset Management**: Consumers track their position in the log, allowing them to replay messages or skip ahead. This means that the messages are not deleted after consumption, allowing for reprocessing.
- **Exactly-once semantics**: Kafka provides strong guarantees about message delivery, even in the presence of failures. Exactly-once means that a message is delivered once and only once, even in the presence of failures. At-least-once means that a message is delivered at least once, but may be delivered multiple times in the presence of failures. At-most-once means that a message is delivered at most once, but may be lost in the presence of failures[2].
- **File-based storage**: Kafka stores messages in a distributed file system, allowing for efficient retrieval and durability. The performance is guaranteed by simple reads and appends to the log files. In such a system, all operations have the complexity of O(1), meaning that the time it takes to perform an operation does not depend on the size of the data set[3].
- **Distributed commit log**: Kafka uses a distributed commit log to ensure that messages are stored in a durable and fault-tolerant manner. This means that messages are written to disk before they are acknowledged, ensuring that they are not lost in the event of a failure.

#### Architecture
- **Producers** publish to **topics**, which are divided into **partitions**
- Messages are written to **brokers**
- **Consumers** fetch data either at their own pace (pull model)
- **Zookeeper** ensures metadata management and leader election


### 2.2 RabbitMQ

#### Problem Addressed

RabbitMQ focuses on flexible routing and reliable delivery of asynchronous messages between decoupled components, suitable for enterprise and microservice architectures[4]. It is used in scenarios where message ordering, routing, and delivery guarantees are critical.

#### Core Principles & Algorithms
RabbitMQ is based on **AMQP (Advanced Message Queuing Protocol)**. Key mechanisms include:
- **Routing Algorithms**: Direct exchange matches messages to queues based on routing keys. Fanout exchange broadcasts messages to all bound queues. Topic exchange allows for wildcard routing. Headers exchange routes messages based on header attributes[4].
- **Message Acknowledgement & Retry**: Consumers acknowledge messages after processing. If a consumer fails, RabbitMQ can requeue the message for another consumer.
- **Delivery Guarantees**: RabbitMQ supports at-most-once and at-least-once delivery semantics. It can also be configured for exactly-once delivery using transactions or publisher confirms.
- **Prefetching**: RabbitMQ allows consumers to prefetch messages, which can improve throughput by reducing round-trip times. This means that the consumer can process multiple messages at once, reducing the time it takes to process each message. 


#### Architecture
- **Producers** send messages to **exchanges**
- **Exchanges** route messages to **queues** based on binding rules
- **Consumers** read messages from queues
- **Clustering** and **HA Queues** provide fault tolerance and scalability
- **Management UI** and **Plugins** for monitoring and extending functionality

---

### 2.3 AWS SNS + SQS

#### Problem Addressed
This combination solves **fan-out messaging** and **durable queueing** in a scalable, serverless context. The main advantage is fully managed services that can handle large volumes of messages without the need for infrastructure management[5].

#### Core Principles & Algorithms
- **SNS (Simple Notification Service)**: push-based, topic-driven pub-sub. It allows you to send messages to multiple subscribers at once, making it ideal for broadcasting messages to multiple recipients.
- **SQS (Simple Queue Service)**: pull-based, decouples components with guaranteed message delivery. It allows you to store messages in a queue until they are processed, ensuring that messages are not lost if the consumer is unavailable.
- Integration pattern:
  - SNS Topic -> Multiple SQS Queues
- Supports **FIFO**, **message deduplication**, and **visibility timeouts**
  - *FIFO* queues ensure that messages are processed in the order they are sent, and that each message is delivered exactly once. This is important for applications where the order of messages matters, such as financial transactions or event processing.
  - *Message deduplication* ensures that duplicate messages are not processed multiple times, which can happen in distributed systems where messages may be sent multiple times due to network failures or other issues.
  - *Visibility timeouts* ensure that messages are not processed multiple times by different consumers. When a consumer receives a message, it has a certain amount of time to process it before the message becomes visible to other consumers. If the consumer fails to process the message within that time, the message is returned to the queue and can be processed by another consumer.

#### Architecture
- **SNS** acts as the event broadcaster
- **SQS** persists messages for later consumption
- Can be integrated with Lambda, EC2, or other AWS services
- Entirely **managed**, with no need to maintain brokers or infrastructure

---

### 2.4 MQTT with Mosquitto

#### Problem Addressed
MQTT solves lightweight messaging challenges in **resource-constrained environments**, especially **IoT**. Mosquitto is a popular open-source MQTT broker that provides a simple and efficient way to implement MQTT in various applications. It is designed for low-bandwidth, high-latency networks, making it ideal for IoT devices and applications where power consumption is a concern[6].

#### Core Principles & Algorithms
- Follows **publish-subscribe**, but optimized for low bandwidth. 
  - Publishers send messages to a broker, which then distributes them to subscribers based on topics.
  - This decouples the sender and receiver, allowing for more flexible communication patterns.
- Quality of Service (QoS) levels:
  - QoS 0: At most once
  - QoS 1: At least once
  - QoS 2: Exactly once
- **Persistent sessions**, **retain flags**, and **last will messages**
  - Persistent sessions allow clients to reconnect and resume their session without losing messages.
  - Retain flags ensure that the last message sent on a topic is stored by the broker and sent to new subscribers.
  - Last will messages are sent by the broker if a client disconnects unexpectedly, allowing for better error handling and notification of failures.

#### Architecture
- **Clients** (sensors/devices) connect to a **Mosquitto broker**
- Topics form a **hierarchical namespace**
- Broker handles session management, routing, and state

---

## 3. Strengths and Weaknesses Analysis

| System       | Strengths                                                                   | Weaknesses                                                                 |
| ------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **Kafka**    | High throughput, scalable, durable, replayable, strong ecosystem            | Complex setup, resource-heavy, no native push (pull model only)            |
| **RabbitMQ** | Flexible routing, plugins, easy integration, mature protocol (AMQP)         | Slower under load, risk of backpressure failures, single-broker limits     |
| **SNS/SQS**  | Fully managed, serverless, scalable, fault-tolerant, integrated with AWS    | Vendor lock-in, delayed visibility, eventual consistency                   |
| **MQTT**     | Lightweight, ideal for IoT, low overhead, power efficient                   | No built-in persistence at scale, limited throughput and monitoring        |
| **Azure SB** | Topic/queue separation, enterprise-grade durability, good Azure integration | Steep learning curve, more config overhead, Azure lock-in, fewer OSS tools |

---

## 4. Conclusion

This analysis highlights the diversity in design trade-offs for message-passing systems. Kafka and RabbitMQ favor flexibility and control at the cost of operational complexity. MQTT excels in constrained environments but lacks high-throughput support. AWS SNS/SQS and Azure Service Bus offer fully managed solutions with scalable and reliable architectures, but with inherent vendor lock-in.

**Azure Service Bus** was chosen for this project because of its seamless integration with other **Azure services**, strong support for **topic-based routing**, and built-in **reliability** features. These align well with the Smart City middleware architecture targeted in the broader research.

**Next Steps**:
- Benchmark Azure Service Bus under varying loads (message size, rate, concurrent clients)
- Compare results with published metrics of other platforms
- Integrate Azure monitoring and diagnostics
- Optionally prototype RabbitMQ or Kafka for comparison

---

## References

1. Kreps, J. (2014). *Benchmarking Apache Kafka: 2 Million Writes Per Second*. [LinkedIn Engineering Blog](https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines)
2. [Message Delivery Guarantees](https://docs.confluent.io/kafka/design/delivery-semantics.html)
3. [Kafka and the File System](https://docs.confluent.io/kafka/design/file-system-constant-time.html)
4. Anubhav Jain, (2023). [RabbitMQ: Concepts and Best Practices](https://medium.com/cwan-engineering/rabbitmq-concepts-and-best-practices-aa3c699d6f08), 
5. Diego Garber, (2023). [SNS + SQS: A match made in the clouds](https://medium.com/slalom-build/sns-sqs-a-match-made-in-the-clouds-c4a53989e007)
6. Eclipse Mosquitto™. [Mosquitto](https://mosquitto.org/)
