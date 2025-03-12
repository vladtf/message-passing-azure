from azure.servicebus import ServiceBusClient as SyncServiceBusClient, ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient as AsyncServiceBusClient
from azure.identity import DefaultAzureCredential as SyncDefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential  # for async operations

class ServiceBusManager:
    def __init__(self, fully_qualified_namespace, topic_name, subscription_name, queue_name):
        # Use separate credentials for sync and async operations.
        self.sync_credential = SyncDefaultAzureCredential()
        self.async_credential = DefaultAzureCredential()
        self.fully_qualified_namespace = fully_qualified_namespace
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.queue_name = queue_name

    def send_message(self, message):
        # Using the synchronous client for sending messages.
        with SyncServiceBusClient(fully_qualified_namespace=self.fully_qualified_namespace, credential=self.sync_credential) as client:
            sender = client.get_topic_sender(topic_name=self.topic_name)
            with sender:
                msg = ServiceBusMessage(message)
                sender.send_messages(msg)

    async def receive_messages(self):
        # Use the async version of the ServiceBusClient for receiving messages.
        async with AsyncServiceBusClient(
            fully_qualified_namespace=self.fully_qualified_namespace,
            credential=self.async_credential,
            logging_enable=True
        ) as client:
            receiver = client.get_queue_receiver(queue_name=self.queue_name)
            async with receiver:
                messages = await receiver.receive_messages(max_message_count=10, max_wait_time=5)
                for msg in messages:
                    # If msg.body is a generator, convert it to a list before joining.
                    if hasattr(msg.body, '__iter__') and not isinstance(msg.body, (bytes, bytearray)):
                        body_bytes = b"".join(list(msg.body))
                    else:
                        body_bytes = msg.body
                    try:
                        print("Received:", body_bytes.decode("utf-8"))
                    except Exception:
                        print("Received:", body_bytes)
                    await receiver.complete_message(msg)
        await self.async_credential.close()
