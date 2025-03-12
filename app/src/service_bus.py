from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.identity import DefaultAzureCredential

class ServiceBusManager:
    def __init__(self, fully_qualified_namespace, topic_name, subscription_name, queue_name):
        credential = DefaultAzureCredential()  # Uses Azure CLI credentials if available
        self.client = ServiceBusClient(fully_qualified_namespace=fully_qualified_namespace, credential=credential)
        self.topic_name = topic_name
        self.subscription_name = subscription_name
        self.queue_name = queue_name

    def send_message(self, message):
        with self.client:
            sender = self.client.get_topic_sender(topic_name=self.topic_name)
            with sender:
                msg = ServiceBusMessage(message)
                sender.send_messages(msg)

    def receive_messages(self):
        messages = []
        with self.client:
            # Read from the queue where messages are forwarded
            receiver = self.client.get_queue_receiver(queue_name=self.queue_name)
            with receiver:
                for msg in receiver:
                    # Decode the message body assuming it is sent as UTF-8 text
                    body = b"".join(msg.body).decode("utf-8")
                    messages.append(body)
                    receiver.complete_message(msg)
        return messages