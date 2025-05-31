# C# Azure Service Bus Performance Test Application

This project demonstrates how to send and receive messages using Azure Service Bus with C#. It mirrors the functionality of the Python application and can be used to compare performance between the two implementations.

## Instructions to Run the C# Application Locally

1. **Open a terminal and navigate to the project folder** (from the root of this repository):
   ```powershell
   cd app-csharp
   ```

2. **Restore dependencies**:
   ```powershell
   dotnet restore
   ```

3. **Build the project**:
   ```powershell
   dotnet build
   ```

4. **Configure your local settings**:
   - Edit `appsettings.json` to provide your Azure Service Bus connection string and entity names (namespace, topic, subscription, queue) as needed for your environment.

5. **Ensure proper Azure role assignments**:
   - The application requires your Azure account (or the service principal it runs as) to have the **Azure Service Bus Data Sender** and **Azure Service Bus Data Receiver** roles on the Service Bus namespace. Without these, the app will not be able to send or receive messages.
   - You can assign these roles using the Azure CLI, for example:
     ```powershell
     $subscriptionId = "<your-subscription-id>"
     $resourceGroup = "<your-resource-group>"
     $namespace = "<your-servicebus-namespace>"
     $userId = (az ad signed-in-user show --query id -o tsv)
     az role assignment create --assignee $userId --role "Azure Service Bus Data Sender" --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ServiceBus/namespaces/$namespace"
     az role assignment create --assignee $userId --role "Azure Service Bus Data Receiver" --scope "/subscriptions/$subscriptionId/resourceGroups/$resourceGroup/providers/Microsoft.ServiceBus/namespaces/$namespace"
     ```

6. **Run the performance test**:
   ```powershell
   dotnet run -- <messages_per_thread> <message_prefix> <mode(write/read/both)>
   ```
   For example, to send 1000 messages per thread with prefix `test` in both write and read modes:
   ```powershell
   dotnet run -- 1000 test both
   ```

## Notes

- Ensure that the Azure Service Bus namespace, topic, subscription, and queue are correctly configured in `appsettings.json` before running locally.
- This application requires .NET 8.0. Make sure it is installed on your system.
- All commands should be run from the `app-csharp` directory unless otherwise specified.
