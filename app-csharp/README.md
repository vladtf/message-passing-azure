# C# Azure Service Bus Performance Test Application

This project demonstrates how to send and receive messages using Azure Service Bus with C#. It mirrors the functionality of the Python application and can be used to compare performance between the two implementations.

## Instructions to Run the C# Application

1. **Navigate to the C# project folder**:
   ```powershell
   cd \app-csharp
   ```

2. **Restore dependencies**:
   ```powershell
   dotnet restore
   ```

3. **Build the project**:
   ```powershell
   dotnet build
   ```

4. **Run the performance test**:
   ```powershell
   dotnet run -- <threads> <messages_per_thread> <message_prefix>
   ```

   For example:
   ```powershell
   dotnet run -- 16 1000 test
   ```

## Notes

- Ensure that the Azure Service Bus namespace, topic, subscription, and queue are correctly configured in the application.
- This application requires .NET 8.0. Make sure it is installed on your system.
