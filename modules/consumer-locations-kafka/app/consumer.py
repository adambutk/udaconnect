import json
import psycopg2
import os
from datetime import datetime
from kafka import KafkaConsumer


KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

DB_NAME = os.environ["DB_NAME"]
DB_PORT = os.environ["DB_PORT"]
DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_SERVER])

def consume_add_location(location):
    session = psycopg2.connect(dbname=DB_NAME, port=DB_PORT, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST)
    cur = session.cursor()

    person_id = int(location["person_id"])
    longitude = float(location["longitude"])
    latitude = float(location["latitude"])
    creation_time = location["creation_time"]

    cur.execute("""
                INSERT INTO location (person_id, coordinate, creation_time) 
                VALUES (%s, ST_point(%s, %s), %s);
                """, (person_id, longitude, latitude, creation_time))

    session.commit()

    # print('Location added to database')

    cur.close()
    session.close()


for message in consumer:
    location_message = json.loads(message.value.decode("utf-8"))
    consume_add_location(location_message)
