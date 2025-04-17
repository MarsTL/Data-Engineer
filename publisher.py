from google.cloud import pubsub_v1
import json
import time


#info for project and topic
project_id = "mov-data-eng"
topic_id = "my-topic"
file_name = "bcsample.json"

#creating a publisher client
publisher = pubsub_v1.PublisherClient()

# topic_path creates  fully qualifiied identifier of the 
# topic path (in form of 'projects/{project_id}/topics/{topics_id}
topic_path = publisher.topic_path(project_id, topic_id)

message_count = 0

start_time = time.time()

#load in the vehical sample
with open(file_name, "r") as f:
    data = json.load(f)

    #publish the record each 
    for record in data:
        message_data = json.dumps(record).encode("utf-8")
        #message_bytes = message_json.encode("utf-8")
        future = publisher.publish(topic_path, data=message_data)
        message_count += 1
        #print(f"published message number {i + 1}: {future.result()}"
#wait for all message to publish
publisher.stop()
end_time = time.time()

print(f"Published {message_count} messages.")
print(f"Time taken to publish: {end_time - start_time:.2f} seconds")
    

#publish 9 messages to the topic
#for n in range(1, 10):
#    data_str = f"Message number {n}"
    #data must be string byte 
#    data = data_str.encode("utf-8")  
    #when you publush a messge, the client returns a future 
#    future = publisher.publish(topic_path, data)
#    print(future.result())

#print(f"Published messages to {topic_path}.")

