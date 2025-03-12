# My Azure Service Bus Application

This project demonstrates how to send and receive messages using Azure Service Bus with Python. It includes a simple application that utilizes the Azure Service Bus SDK to manage message operations.

## Project Structure

```
my-azure-servicebus-app
├── src
│   ├── app.py               # Entry point of the application
│   └── service_bus.py       # Contains ServiceBusManager class for message operations
├── tests
│   └── test_service_bus.py   # Unit tests for ServiceBusManager
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd my-azure-servicebus-app
   ```

2. **Create a virtual environment using Pipenv:**
   ```
   pipenv install
   ```

3. **Enter the Pipenv shell:**
   ```
   pipenv shell
   ```

4. **Assign the Azure Service Bus Data Sender and Receiver roles:**

   ```powershell
   # Variables
   $subscriptionId = "01810409-8e44-41af-a73f-b47942986098"
   $resourceGroup = "soam-rg"
   $namespace = "soam-sb-namespace"

   # Get the signed-in user's object ID
   $userId = (az ad signed-in-user show --query id -o tsv)

   # Assign the Azure Service Bus Data Sender role
   az role assignment create --assignee $userId --role "Azure Service Bus Data Sender" --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ServiceBus/namespaces/$namespace"

   # Assign the Azure Service Bus Data Receiver role
   az role assignment create --assignee $userId --role "Azure Service Bus Data Receiver" --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ServiceBus/namespaces/$namespace"
   ```

5. **Use the application:**

   To send a message:
   ```
   python src/app.py send "Your message here"
   ```

   To receive messages:
   ```
   python src/app.py receive
   ```

## Usage

To send a message to the Service Bus, run the following command:
```
python src/app.py send "Your message here"
```

To receive messages from the Service Bus, run:
```
python src/app.py receive
```

## Running Tests

To run the unit tests for the `ServiceBusManager`, use:
```
pytest tests/test_service_bus.py
```

## License

This project is licensed under the MIT License.