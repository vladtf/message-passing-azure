# Message Passing Performance Project: Technical Report 1

## Table of Contents

- [Message Passing Performance Project: Technical Report 1](#message-passing-performance-project-technical-report-1)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Description of Existing Solutions](#2-description-of-existing-solutions)
    - [Apache Kafka](#apache-kafka)
    - [RabbitMQ](#rabbitmq)
    - [AWS SNS + SQS](#aws-sns--sqs)
    - [MQTT with Mosquitto](#mqtt-with-mosquitto)
  - [3. Strengths and Weaknesses Analysis](#3-strengths-and-weaknesses-analysis)
  - [4. Conclusion](#4-conclusion)
  - [References](#references)


## 1. Introduction

This project focuses on **message passing performance** in distributed systems, specifically using **Azure Service Bus**. The rationale for this choice is to explore the capabilities of **Azure Service Bus** as a message broker in a distributed architecture. I want to integrate this solution to my dissertation project, which focuses on building a Smart City middleware platform. Specifically, I will be using **Azure Service Bus** to facilitate communication between sensors and the middleware platform, eventually to handle the communication between the components of the platform itself. The goal is to evaluate the performance of message passing in a distributed system and provide an optimized architecture for large-scale applications.

The project will simulate a **publish-subscribe** messaging pattern, where messages are sent from a sensor (publisher) to a middleware platform (subscriber) via **Azure Service Bus**. To match the **SNS** + **SQS** architecture, the project will utilize **Service Bus Topics** as entry points for messages and **Service Bus Queues** to store messages for processing.

## 2. Description of Existing Solutions

### Apache Kafka

Apache Kafka is a distributed event streaming platform capable of handling millions of events per second. It is designed for high throughput and low latency, making it suitable for real-time data processing. Kafka uses a publish-subscribe model, where producers send messages to topics, and consumers read from those topics [1].

The architecture of Kafka consists of the following components:
1. **Producers** – Applications that send messages to Kafka topics.
2. **Consumers** – Applications that read messages from Kafka topics.
3. **Topics** – Categories to which messages are published.
4. **Brokers** – Kafka servers that store and manage topics.
5. **Zookeeper** – A centralized service for maintaining configuration information and providing distributed synchronization.
6. **Partitions** – Each topic can be divided into multiple partitions for parallel processing.


All these components allows Kafka to achieve high throughput and low latency. Kafka is designed to handle large volumes of data and can scale horizontally by adding more brokers to the cluster. It also provides features like replication, fault tolerance, and message retention.

### RabbitMQ

Problem: General-purpose messaging with rich routing semantics.

Core Principles: Message queues, exchanges (direct, topic, fanout), ACKs, and retries.

Architecture: Broker-based architecture built on AMQP (Advanced Message Queuing Protocol).


### AWS SNS + SQS

Problem: Fan-out messaging and decoupled message persistence.

Core Principles: SNS for topic-based pub-sub; SQS for queue-based delivery; durable, scalable.

Architecture: Serverless integration, cross-region, FIFO or standard queues.


### MQTT with Mosquitto

Problem: Lightweight messaging for IoT devices.

Core Principles: Publish/subscribe, topic hierarchy, persistent sessions, QoS.

Architecture: Minimal footprint broker; clients connect over TCP with low overhead.


## 3. Strengths and Weaknesses Analysis

| System      | Strengths                                                         | Weaknesses                                                       |
| ----------- | ----------------------------------------------------------------- | ---------------------------------------------------------------- |
| Kafka       | High throughput, durable, scalable, replayable log                | Higher latency, harder setup, no direct push, limited for IoT    |
| RabbitMQ    | Flexible routing, good for enterprise apps, supports plugins      | Slower under high load, can crash under backpressure             |
| AWS SNS/SQS | Fully managed, integrated with AWS, serverless, fan-out supported | Cross-cloud latency, vendor lock-in, limited delivery guarantees |
| MQTT        | Lightweight, ideal for IoT, low power/network overhead            | Not suited for high-throughput or persistent workloads           |
| Azure SB    | Strong integration with Azure, durable, topic/queue support       | More complex configuration, less community support than Kafka    |

## 4. Conclusion

Each messaging solution makes trade-offs in throughput, flexibility, and delivery guarantees.

Azure Service Bus offers strong integration, durability, and topic/queue support, comparable to SNS + SQS but with more complex configuration.

The most most important aspect of Azure Service Bus is its integration with Azure services, which can be easily used in my dissertation project that focuses on building a Smart City middleware platform using Azure services. This integration allows for seamless communication between various components of the platform, such as sensors, data processing units, and storage solutions.

The next steps in the project will involve benchmarking the performance of Azure Service Bus and finding the optimal configuration for my use case. This will include testing different message sizes, throughput levels, and configurations to identify the best setup for my specific requirements. Additionally, I will explore the integration of Azure Service Bus with other Azure services to enhance the overall architecture of the Smart City middleware platform.


## References

- [1] Benchmarking Apache Kafka: 2 Million Writes Per Second (On Three Cheap Machines) - https://engineering.linkedin.com/kafka/benchmarking-apache-kafka-2-million-writes-second-three-cheap-machines

