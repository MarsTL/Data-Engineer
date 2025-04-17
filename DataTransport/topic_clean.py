from google.cloud import pubsub_v1

project_id = "mov-data-eng"
subscription_id = "my-sub"
topic_id = "my-topic"

#client object created for sub and topic intereaction
#delete & create subscription
subscriber = pubsub_v1.SubscriberClient()
#get topic path needed when recreating the subscription
publisher = pubsub_v1.PublisherClient()

#fulll name for pub/sub api
subscription_path = subscriber.subscription_path(project_id, subscription_id)
topic_path = publisher.topic_path(project_id, topic_id)

# Delete the subscription to clear any message backlog
try:
    subscriber.delete_subscription(request={"subscription": subscription_path})
    print(f"Deleted subscription: {subscription_path}")
except Exception as e:
    print(f"Error deleting subscription: {e}")

# Recreate the subscription to continue listening to the topic
try:
    subscriber.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )
    print(f"Recreated subscription: {subscription_path}")
except Exception as e:
    print(f"Error creating subscription: {e}")

