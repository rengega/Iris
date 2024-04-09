import json

from flask_socketio import SocketIO
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import paho.mqtt.client as mqtt
import paho
from dash import dash_table

# Initialize the MQTT client
mqtt_client = mqtt.Client(client_id="DASHsubscriber", userdata=None, protocol=paho.mqtt.client.MQTTv5, transport="tcp")
mqtt_client.username_pw_set("renild", "adminADMIN")
mqtt_client.connect("c8e848e89323403bb701fd7ead3f915f.s1.eu.hivemq.cloud", 8883)
mqtt_client.subscribe("iris/#", qos=1)


