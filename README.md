# Message Passing Performance Project

This project demonstrates a message passing architecture utilizing Azure Service Bus. Infrastructure is provisioned using Terraform, and a Python application is provided for sending and receiving messages.

## Table of Contents

- [Message Passing Performance Project](#message-passing-performance-project)
  - [Table of Contents](#table-of-contents)
  - [Project Structure](#project-structure)
  - [Prerequisites](#prerequisites)
  - [Terraform Infrastructure Setup](#terraform-infrastructure-setup)
    - [Steps to Provision Infrastructure](#steps-to-provision-infrastructure)
  - [Python Application Setup](#python-application-setup)
    - [Configuration](#configuration)
    - [Role Assignment](#role-assignment)
    - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)


## Project Structure

```
message-passing-perf
├── app                         # Python application for sending and receiving messages  
└── terraform                   # Terraform configuration for provisioning Azure resources
```

## Prerequisites

- **Azure Subscription:** An active Azure subscription.
- **Terraform:** [Terraform CLI](https://www.terraform.io/downloads.html).
- **Azure CLI:** [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) (must be logged in with `az login`).
- **Pipenv:** [Pipenv](https://pipenv.pypa.io/en/latest/) for managing Python environments.

## Terraform Infrastructure Setup

The Terraform configuration provisions the following Azure resources:
- **Resource Group** (`soam-rg`)
- **Service Bus Namespace** (`soam-sb-namespace`)
- **Service Bus Topic** (`soam-topic`)
- **Service Bus Queue** (`soam-queue`) – to which messages are forwarded
- **Service Bus Subscription** (`soam-subscription`) – forwards messages from the topic to the queue
- *(Optional)* Authorization rule for the topic

### Steps to Provision Infrastructure

1. Navigate to the `terraform` folder:
   ```
   cd terraform
   ```

2. Initialize Terraform:
   ```
   terraform init
   ```

3. Preview the infrastructure changes:
   ```
   terraform plan
   ```

4. Apply the configuration:
   ```
   terraform apply
   ```

## Python Application Setup

The Python application sends messages to the Service Bus Topic and receives forwarded messages from the Service Bus Queue.

### Configuration

Edit the `config.ini` file in the `app` folder to specify your Service Bus settings:

```ini
[servicebus]
# Fully qualified namespace, e.g. soam-sb-namespace.servicebus.windows.net
fully_qualified_namespace = soam-sb-namespace.servicebus.windows.net
topic_name = soam-topic
subscription_name = soam-subscription
queue_name = soam-queue
```

### Role Assignment

Before running the application, ensure your account has the necessary permissions:

```powershell
# Variables
$subscriptionId = "01810409-8e44-41af-a73f-b47942986098"
$resourceGroup = "soam-rg"
$namespace = "soam-sb-namespace"

# Get the signed-in user's object ID (or use your email directly as the identifier)
$userId = (az ad signed-in-user show --query objectId -o tsv)

# Assign the Azure Service Bus Data Sender role
az role assignment create --assignee $userId --role "Azure Service Bus Data Sender" --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ServiceBus/namespaces/$namespace"

# Assign the Azure Service Bus Data Receiver role
az role assignment create --assignee $userId --role "Azure Service Bus Data Receiver" --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ServiceBus/namespaces/$namespace"
```

### Running the Application

1. Navigate to the `app` folder:
   ```
   cd app
   ```

2. Install dependencies and enter the Pipenv shell:
   ```
   pipenv install
   pipenv shell
   ```

3. **Send a message:**
   ```
   python src/app.py send "Your message here"
   ```

4. **Receive messages:**  
   This command reads messages from the queue and displays them.
   ```
   python src/app.py receive
   ```

## Running Tests

To run the unit tests for the Python application, execute:
```
pytest tests/test_service_bus.py
```


