from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
import time

# TODO(developer)
project_id = "mov-data-eng"
subscription_id = "my-sub"
#timeout = None
message_goal = 6218

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

message_count = 0
start_time = time.time()

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    global message_count
    message_count += 1
    message.ack()
    if message_count % 100000 == 0:
        print(f"Recieved {message_count} message so far...")
    #message.ack()

    if message_count >= message_goal:
        streaming_pull_future.cancel()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        #streaming_pull_future.result(timeout=timeout)
        
        streaming_pull_future.result()

    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.

end_time = time.time()
print(f"\nReceived total: {message_count} messages.")
print(f"Time taken to consume: {end_time - start_time:.2f} seconds")
