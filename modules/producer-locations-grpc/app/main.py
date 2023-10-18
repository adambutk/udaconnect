import time
import json
import os

from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from kafka import KafkaProducer


KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        # todo: create location in db
        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
            "creation_time": request.creation_time,
        }
        # comment out print in production
        print(request_value)

        # forward request to kafka consumer
        bytes_value = json.dumps(request_value).encode('utf-8')
        producer.send(KAFKA_TOPIC, bytes_value)
        producer.flush()

        return location_pb2.Location(**request_value)


# Initialize gRPC server
# Set max_workers to control the number of threads that can be used concurrently
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
