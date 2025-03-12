import sys
import os
from service_bus import ServiceBusManager

def main():
    if len(sys.argv) < 2:
        print("Usage: python app.py <send|receive> [message]")
        sys.exit(1)

    command = sys.argv[1]

    # Retrieve connection details from environment variables
    connection_string = os.environ.get("SERVICE_BUS_CONNECTION_STRING")
    topic_name = os.environ.get("SERVICE_BUS_TOPIC_NAME")
    subscription_name = os.environ.get("SERVICE_BUS_SUBSCRIPTION_NAME")

    if not all([connection_string, topic_name, subscription_name]):
        print("Missing required environment variables. Please set SERVICE_BUS_CONNECTION_STRING, SERVICE_BUS_TOPIC_NAME, and SERVICE_BUS_SUBSCRIPTION_NAME.")
        sys.exit(1)

    sb_manager = ServiceBusManager(connection_string, topic_name, subscription_name)

    if command == "send":
        if len(sys.argv) < 3:
            print("Usage: python app.py send 'Your message here'")
            sys.exit(1)
        message = sys.argv[2]
        sb_manager.send_message(message)
    elif command == "receive":
        sb_manager.receive_messages()
    else:
        print("Unknown command. Use 'send' or 'receive'.")

if __name__ == '__main__':
    main()