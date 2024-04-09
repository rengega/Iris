import csv
import logging
import threading
import time

import paho
import paho.mqtt.client as mqtt
import json

class IrisPublisher:
    mqtt_client = None
    dataset = None

    def __init__(self):
        self.mqtt_client = mqtt.Client(client_id="publisher", userdata=None, protocol=paho.mqtt.client.MQTTv5, transport="tcp")
        self.mqtt_client.username_pw_set("renild", "adminADMIN")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.tls_set(tls_version=paho.mqtt.client.ssl.PROTOCOL_TLS, cert_reqs=paho.mqtt.client.ssl.CERT_NONE)
        self.mqtt_client.connect("c8e848e89323403bb701fd7ead3f915f.s1.eu.hivemq.cloud", 8883)
        try :
            self.dataset = open('dataset.csv', 'r')
            print("File opened successfully")
        except FileNotFoundError:
            logging.error("File not found")
            exit(1)


    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("IRIS_PUBLISHER: CONNACK received with code %s." % rc)

    def on_publish(self, client, userdata, mid, properties=None):
        print("mid: " + str(mid))


    def stop_connection(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("IRIS_PUBLISHER: Connection stopped.")
        exit(0)

    # Method to start the loop that reads the CSV file and publishes the
    # records to the MQTT topics named after the "species" field
    def start_loop(self):
        self.mqtt_client.loop_start()

        reader = csv.reader(self.dataset)
        header = next(reader)
        while True:
            self.dataset.seek(0)
            # Skip the header
            next(reader)
            for row in reader:  # Serialize the row to a JSON string and publish it
                # Create a dictionary from the row
                record = dict(zip(header, row))
                # Add timestamp field to the record
                record["acquisition_timestamp"] = time.time()
                # Convert the dictionary to a JSON string
                json_record = json.dumps(record)
                print(f"IRIS_PUBLISHER: Publishing record: {json_record}")
                # Publish the JSON string to the MQTT topic named after the species
                topic = record.get("species")
                self.mqtt_client.publish("iris/" + topic, json_record, qos=1)
                time.sleep(2)
