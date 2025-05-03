# perf.py
import os, sys, time, asyncio
from service_bus_manager_async import AsyncServiceBusManager
from azure.servicebus.aio import ServiceBusSender
import configparser
from azure.servicebus import ServiceBusMessage, ServiceBusReceiveMode, ServiceBusReceivedMessage
from azure.servicebus.exceptions import ServiceBusError

def load_config():
    config = configparser.ConfigParser()
    # Locate the config.ini file relative to this file
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.ini")
    if not os.path.isfile(config_path):
        print(f"Config file not found at {config_path}")
        sys.exit(1)
    config.read(config_path)
    return config

async def perf(threads: int, per_thread: int, base: str, fully_qualified_namespace: str, topic_name: str, subscription_name: str, queue_name: str):
    sb = AsyncServiceBusManager(
        fully_qualified_namespace=fully_qualified_namespace,
        topic_name=topic_name,
        subscription_name=subscription_name,
        queue_name=queue_name,
        prefetch=1000,
    )

    try:
        # ---------- writers ---------------------------------------------------
        async def writer(idx: int):
            payloads = [f"{base} T{idx} #{i}" for i in range(per_thread)]
            async with sb._client.get_topic_sender(sb._topic_name) as sender:
                await _send_payloads(sender, payloads)

        async def _send_payloads(sender: ServiceBusSender, bodies):
            batch = await sender.create_message_batch()
            for body in bodies:
                try:
                    batch.add_message(ServiceBusMessage(body))  # 1 hour TTL
                except ValueError:  # Batch full → flush & start a new one
                    await sender.send_messages(batch)
                    batch = await sender.create_message_batch()
                    batch.add_message(ServiceBusMessage(body))
            if len(batch):  # Send the tail
                await sender.send_messages(batch)



        t0 = time.perf_counter()
        await asyncio.gather(*(writer(i) for i in range(threads)))
        dt = time.perf_counter() - t0
        total = threads * per_thread
        print(f"Sent {total:,} messages in {dt:.2f}s  →  {total/dt:,.0f} msg/s")\
        
        # sleep a bit to let the messages settle
        print("Sleeping for 15 seconds to let messages settle...")
        await asyncio.sleep(15)

        # ---------- readers ---------------------------------------------------
        async def reader(idx: int, out: list):
            async with sb._client.get_queue_receiver(
                    sb._queue_name,
                    prefetch_count=4000,
                    max_wait_time=1,
                    receive_mode=ServiceBusReceiveMode.RECEIVE_AND_DELETE
            ) as rx:
                while True:
                    batch = await rx.receive_messages(4000, max_wait_time=1)
                    if not batch:
                        break
                    out.extend(batch)

        received: list[ServiceBusReceivedMessage] = []
        t1 = time.perf_counter()
        await asyncio.gather(*(reader(i, received) for i in range(threads)))
        dt = time.perf_counter() - t1
        print(f"Read {len(received):,} messages in {dt:.2f}s → {len(received)/dt:,.0f} msg/s")
    finally:
        await sb.close()  # Ensure proper cleanup of resources

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python perf.py <threads> <messages_per_thread> <message_prefix>")
        sys.exit(1)

    th  = int(sys.argv[1])
    per = int(sys.argv[2])
    pre = sys.argv[3]
    
    config = load_config()
    
    fully_qualified_namespace = config.get("servicebus", "fully_qualified_namespace")
    topic_name = config.get("servicebus", "topic_name")
    subscription_name = config.get("servicebus", "subscription_name")
    queue_name = config.get("servicebus", "queue_name")
    print(f"Using Service Bus: fully_qualified_namespace={fully_qualified_namespace}, topic_name={topic_name}, subscription_name={subscription_name}, queue_name={queue_name}")

    asyncio.run(perf(th, per, pre, fully_qualified_namespace, topic_name, subscription_name, queue_name))
    print("Performance test completed.")
