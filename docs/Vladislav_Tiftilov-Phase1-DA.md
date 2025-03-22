# Message Passing Performance Project: Technical Report 1

## Table of Contents

- [Message Passing Performance Project: Technical Report 1](#message-passing-performance-project-technical-report-1)
  - [Table of Contents](#table-of-contents)
  - [1. Introduction](#1-introduction)
  - [2. Technical Specifications](#2-technical-specifications)
    - [Technologies Used](#technologies-used)
    - [Comparison of Alternatives](#comparison-of-alternatives)
  - [3. Initial Design](#3-initial-design)
    - [Architecture Overview](#architecture-overview)
    - [System Diagram](#system-diagram)
    - [Infrastructure Setup](#infrastructure-setup)
    - [Initial Testing Results](#initial-testing-results)
  - [4. Conclusion](#4-conclusion)
    - [Achievements](#achievements)
    - [Next Steps](#next-steps)


## 1. Introduction

This project focuses on **message passing performance** in distributed systems, specifically using **Azure Service Bus**. The rationale for this choice is to explore the capabilities of **Azure Service Bus** as a message broker in a distributed architecture. I want to integrate this solution to my dissertation project, which focuses on building a Smart City middleware platform. Specifically, I will be using **Azure Service Bus** to facilitate communication between sensors and the middleware platform, eventually to handle the communication between the components of the platform itself. The goal is to evaluate the performance of message passing in a distributed system and provide an optimized architecture for large-scale applications.

The project will simulate a **publish-subscribe** messaging pattern, where messages are sent from a sensor (publisher) to a middleware platform (subscriber) via **Azure Service Bus**. To match the **SNS** + **SQS** architecture, the project will utilize **Service Bus Topics** as entry points for messages and **Service Bus Queues** to store messages for processing.

## 2. Technical Specifications

### Technologies Used

| **Component**          | **Technology**        | **Reasoning**                                                    |
| ---------------------- | --------------------- | ---------------------------------------------------------------- |
| Cloud Provider         | **Azure**             | Provides managed **Service Bus** for message passing             |
| Messaging Service      | **Azure Service Bus** | Supports **asynchronous message processing** via Topics & Queues |
| Infrastructure as Code | **Terraform**         | Automates **cloud infrastructure deployment**                    |
| Programming Language   | **Python**            | Suitable for **scripting, automation, and cloud interactions**   |
| CLI Tooling            | **Azure CLI**         | Required for managing **Azure Service Bus and role assignments** |
| Testing Framework      | **Locust**            | Enables **load testing** of the message passing system           |
| Dependency Management  | **Pipenv**            | Simplifies **Python package management**                         |

### Comparison of Alternatives

| **Technology**    | **Alternative** | **Why Not Used?**                                                                                          |
| ----------------- | --------------- | ---------------------------------------------------------------------------------------------------------- |
| Azure Service Bus | Apache Kafka    | Kafka is optimized for **log-based streaming**, while **Service Bus is better for event-driven messaging** |
| Terraform         | Azure Bicep     | Terraform supports **multi-cloud** and has **better modularization**                                       |
| Python            | Go / Java       | Python offers **faster prototyping and better cloud SDK support**                                          |

## 3. Initial Design

### Architecture Overview

The system consists of:
1. **Azure Service Bus Namespace** – The message broker.
2. **Service Bus Topic** – Handles published messages.
3. **Service Bus Queue** – Messages are forwarded here.
4. **Python Application** – Sends & receives messages.

### System Diagram

<img src="assets/architecture_diagram.png" alt="Architecture Diagram" width="100%"/>

### Infrastructure Setup

**Terraform Deployment**
```sh
cd terraform
terraform init
terraform apply
```

**Python Application Setup**
```sh
cd app
pipenv install
pipenv shell
```

**Sending Messages**
```sh
python src/app.py send "Hello, world!"
```

**Receiving Messages**
```sh
python src/app.py receive
```

**Performance Testing**
```sh
python app.py perf <threads> <messages_per_thread> 'message prefix'
``` 

### Initial Testing Results

| **Action** | **Messages** | **Time (seconds)** | **Throughput (msg/s)** |
| ---------- | ------------ | ------------------ | ---------------------- |
| Sent       | 40           | 81.38              | 0.49                   |
| Read       | 40           | 5.92               | 6.76                   |

## 4. Conclusion
### Achievements

- Successfully deployed a **distributed message passing system** using **Azure Service Bus**.  
- Validated **message sending and receiving functionality**.  
- Automated infrastructure deployment via **Terraform**.
- Conducted initial performance tests.

### Next Steps

- **Optimize Performance** – Measure **latency and throughput**.  
- **Add Message Batching** – Improve efficiency with **bulk processing**.  
- **Compare with Alternatives** – Evaluate performance against other messaging systems.
- **Integrate Locust** – Perform **load testing** to evaluate system under stress.
- **Documentation** – Create comprehensive documentation for the system.

