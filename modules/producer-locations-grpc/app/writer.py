import grpc
import location_pb2
import location_pb2_grpc
from datetime import datetime

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:5005")
dummy_location = location_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
location = location_pb2.Location(
    person_id=1,
    longitude="34.77946",
    latitude="32.40343",
    creation_time="2020-07-07 13:37:01",
)

# todo: add LocationId request

response = dummy_location.Create(location)
