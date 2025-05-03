"""
Efficient, fully-async wrapper around the Azure Service Bus Python SDK.
• Creates ONE connection, ONE sender, ONE receiver – reused for the whole run.
• Supports batch sends and high-bandwidth receives.
"""

from azure.servicebus.aio import ServiceBusClient as AsyncServiceBusClient
from azure.servicebus import ServiceBusMessage, TransportType, ServiceBusReceiveMode
from azure.servicebus.exceptions import ServiceBusError
from azure.identity import DefaultAzureCredential as SyncDefaultAzureCredential
from azure.identity.aio import DefaultAzureCredential  # for async operations


class AsyncServiceBusManager:
    """
    Parameters
    ----------
    connection_str : str
        Full Service Bus connection string (typically the “RootManageSharedAccessKey” one).
    queue_name : str
        Queue you want to test; change to topic/subscription if needed.
    prefetch : int, optional
        Messages to pre-pull into the link credit window. 100–500 is a sweet spot.
    """

    def __init__(self, fully_qualified_namespace: str,topic_name: str, subscription_name: str, queue_name: str, prefetch: int = 100):
        try:
            # Single TCP + AMQP session for everything.
            self.async_credential = DefaultAzureCredential()
            self.sync_credential = SyncDefaultAzureCredential()

            self._client = AsyncServiceBusClient(
                fully_qualified_namespace=fully_qualified_namespace,
                credential=self.async_credential,
                logging_enable=False,               # for debugging
                transport_type=TransportType.Amqp,  # for Azure Functions
            )
            self._queue_name = queue_name
            self._topic_name = topic_name
            self._receiver = self._client.get_queue_receiver(
                queue_name=self._queue_name,
                max_wait_time=1,                  # seconds
                prefetch_count=prefetch,            # pre-pull messages into the link credit window
                receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE
            )
        except Exception as e:
            raise ServiceBusError(f"Failed to initialize ServiceBusManager: {e}")

    # ------------------------------------------------------------------ send
    async def send_batch(self, bodies: list[str]):
        """
        Send N messages using the minimum number of AMQP frames.
        """
        try:
            async with self._sender:
                batch = await self._sender.create_message_batch()
                for body in bodies:
                    try:
                        batch.add_message(ServiceBusMessage(body, time_to_live=3600))  # 1 hour TTL
                    except ValueError:               # batch full → flush & start a new one
                        await self._sender.send_messages(batch)
                        batch = await self._sender.create_message_batch()
                        batch.add_message(ServiceBusMessage(body))
                if len(batch):                       # send the tail
                    await self._sender.send_messages(batch)
        except ServiceBusError as e:
            raise ServiceBusError(f"Failed to send batch: {e}")

    # ---------------------------------------------------------------- receive
    async def drain(self) -> list[str]:
        """
        Pull **all** available messages and return their bodies as strings.
        """
        msgs, consecutive_empty = [], 0
        async with self._receiver:
            while True:
                batch = await self._receiver.receive_messages(
                                   max_message_count=1000,          # pull more at once
                                   max_wait_time=1
                               )
                if batch:
                    msgs.extend(batch)
                    consecutive_empty = 0
                else:
                    consecutive_empty += 1
                    if consecutive_empty >= 3:      # ~3 s idle ⇒ done
                        break

        return [b"".join(p for p in m.body).decode() for m in msgs]


    # ---------------------------------------------------------------- close
    async def close(self):
        # Ensure proper cleanup of the ServiceBusClient and credential
        await self._client.close()
        await self.async_credential.close()  # Explicitly close the credential to avoid unclosed session warnings
