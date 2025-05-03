# Message Passing Performance Project: Technical Report 2

## Table of Contents

- [Message Passing Performance Project: Technical Report 2](#message-passing-performance-project-technical-report-2)
  - [Table of Contents](#table-of-contents)
  - [TODO](#todo)

---

## TODO

Increasing the number of threads improves performance.

```bash
➜  python src/app.py perf 20 20  test
Clearing queue before starting performance testing...
Starting performance testing...
Threads: 20, Messages per thread: 20
Sent 400 messages in 112.80 seconds.
Write Throughput: 3.55 messages/second.
Measuring read performance: reading messages from the queue...
Read 400 messages in 11.41 seconds.
Read Throughput: 35.07 messages/second.
```

Batching messages and moving from threads to asyncio-based approach improves performance.

```bash
@vtiftilov [D:\personal\message-passing-perf\app] git(main)
➜  python src/app.py 16 1000 test
Using Service Bus: fully_qualified_namespace=soam-sb-namespace.servicebus.windows.net, topic_name=soam-topic, subscription_name=soam-subscription, queue_name=soam-queue
Sent 16,000 messages in 26.80s  →  597 msg/s
Read 94,969 messages in 384.63s →  247 msg/s
Performance test completed.
```

Upgrading the Azure Service Bus to Premium tier improves performance.

```bash
➜  python src/app.py 16 4000 test
Using Service Bus: fully_qualified_namespace=soam-sb-namespace.servicebus.windows.net, topic_name=soam-topic, subscription_name=soam-subscription, queue_name=soam-queue
Sent 64,000 messages in 16.40s  →  3,902 msg/s
Sleeping for 15 seconds to let messages settle...
Read 64,000 messages in 109.40s → 585 msg/s
Performance test completed.
```
