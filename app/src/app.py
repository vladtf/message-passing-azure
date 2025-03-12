import sys
import os
import configparser
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

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py <send|receive> [message]")
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
        messages = sb_manager.receive_messages()
        for m in messages:
            print(m)
    else:
        print("Unknown command. Use 'send' or 'receive'.")

if __name__ == '__main__':
    main()