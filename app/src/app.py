import sys
import os
import configparser
import threading
import time
from service_bus import ServiceBusManager

def load_config():
    config = configparser.ConfigParser()
    # Locate the config.ini file relative to this file
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.ini")
    if not os.path.isfile(config_path):
        print(f"Config file not found at {config_path}")
        sys.exit(1)
    config.read(config_path)
    return config

async def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py <send|receive|perf> [options]")
        sys.exit(1)

    command = sys.argv[1]
    config = load_config()

    try:
        fully_qualified_namespace = config.get("servicebus", "fully_qualified_namespace")
        topic_name = config.get("servicebus", "topic_name")
        subscription_name = config.get("servicebus", "subscription_name")
        queue_name = config.get("servicebus", "queue_name")
    except Exception as e:
        print(f"Error reading configuration: {e}")
        sys.exit(1)

    sb_manager = ServiceBusManager(fully_qualified_namespace, topic_name, subscription_name, queue_name)

    if command == "send":
        if len(sys.argv) < 3:
            print("Usage: python app.py send 'Your message here'")
            sys.exit(1)
        message = sys.argv[2]
        sb_manager.send_message(message)
    elif command == "receive":
        await sb_manager.receive_messages()
    elif command == "perf":
        if len(sys.argv) < 5:
            print("Usage: python app.py perf <threads> <messages_per_thread> 'message prefix'")
            sys.exit(1)
        try:
            threads_count = int(sys.argv[2])
            messages_per_thread = int(sys.argv[3])
        except ValueError:
            print("Threads and messages_per_thread must be integers.")
            sys.exit(1)
        base_message = sys.argv[4]

        # Clear the queue before starting performance testing.
        print("Clearing queue before starting performance testing...")
        sb_manager.clear_queue()

        def thread_function(thread_id):
            for i in range(messages_per_thread):
                msg = f"{base_message} from thread {thread_id} message {i}"
                sb_manager.send_message(msg)

        threads = []
        start_time = time.time()
        for i in range(threads_count):
            t = threading.Thread(target=thread_function, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        end_time = time.time()
        total_messages = threads_count * messages_per_thread
        print(f"Sent {total_messages} messages in {end_time - start_time:.2f} seconds.")

        # Read performance: measure how long it takes to read all messages
        print("Measuring read performance: reading messages from the queue...")
        start_read = time.time()
        messages = sb_manager.read_all_messages()
        end_read = time.time()
        print(f"Read {len(messages)} messages in {end_read - start_read:.2f} seconds.")
    else:
        print("Unknown command. Use 'send', 'receive', or 'perf'.")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())