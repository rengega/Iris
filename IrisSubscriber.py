import datetime
import paho
import paho.mqtt.client as mqtt
import json

class IrisSubscriber:
    mqtt_client = None
    global shared_queue
    def __init__(self, shared_queue):
        self.mqtt_client = mqtt.Client(client_id="subscriber", userdata=None, protocol=paho.mqtt.client.MQTTv5, transport="tcp")
        self.mqtt_client.username_pw_set("renild", "adminADMIN")
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.tls_set(tls_version=paho.mqtt.client.ssl.PROTOCOL_TLS, cert_reqs=paho.mqtt.client.ssl.CERT_NONE)
        self.mqtt_client.connect("c8e848e89323403bb701fd7ead3f915f.s1.eu.hivemq.cloud", 8883)
        self.shared_queue = shared_queue


    def start(self, topic = "#"):
        self.mqtt_client.subscribe("iris/" + topic, qos=1)
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc, properties=None):
        print("IRIS_SUBSCRIBER: CONNACK received with code %s." % rc)


    def stop_connection(self):
        self.mqtt_client.loop_stop()
        self.mqtt_client.disconnect()
        print("IRIS_SUBSCRIBER: Connection stopped.")
        exit(0)


    # The subscriber will deserialize and add the incoming messages to a CSV file
    def on_message(self, client, userdata, msg):
        print("IRIS_SUBSCRIBER: New message on " + "topic : " + " "  + msg.topic + " "  + " QoS: " + str(msg.qos) + " Payload " + str(msg.payload))
        try:
            data = json.loads(msg.payload.decode("utf-8"))  # Decode the JSON payload
            data["acquisition_timestamp"] = datetime.datetime.fromtimestamp(data["acquisition_timestamp"]).strftime('%Y-%m-%d %H:%M:%S')
            print(f"IRIS_SUBSCRIBER: Dataload from MQTT: {data}")
            # add the data to the shared queue
            self.shared_queue.append(data)
        except Exception as e:
            print(f"IRIS_SUBSCRIBER: Error while posting to the shared queue: {e}")

