from azure.servicebus import ServiceBusClient, ServiceBusMessage


class ServiceBusManager:
    def __init__(self, connection_string, topic_name, subscription_name):

        self.client = ServiceBusClient.from_connection_string(connection_string)
        self.topic_name = topic_name
        self.subscription_name = subscription_name

    def send_message(self, message):
        with self.client:
            sender = self.client.get_topic_sender(self.topic_name)
            with sender:
                msg = ServiceBusMessage(message)
                sender.send_messages(msg)

    def receive_messages(self):
        messages = []
        with self.client:
            receiver = self.client.get_subscription_receiver(self.topic_name, self.subscription_name)
            with receiver:
                for msg in receiver:
                    messages.append(str(msg))
                    receiver.complete_message(msg)
        return messages
