import paho.mqtt.client as mqtt
import subprocess
import json
import time

# ---- Configuration ----
BROKER = "mqttadress"   # Change to your MQTT broker
PORT = 1883                      # Change to your broker port if not 1883
USERNAME = "username"                 # If required
PASSWORD = "passwrd"                 # If required
CLIENT_ID = "windows_pc_switch"
HA_DISCOVERY_PREFIX = "homeassistant"

# ---- Switch Configuration ----
SWITCH_NAME = "windows_pc_power"
COMMAND_TOPIC = f"home/{SWITCH_NAME}/set"
STATE_TOPIC = f"home/{SWITCH_NAME}/state"
UNIQUE_ID = "windows_pc_switch_01"

# Commands to run for ON/OFF
COMMAND_ON = ["C:\DisplaySwitch\wsds.exe desk.dis"] # Example “on” command
COMMAND_OFF = ["C:\DisplaySwitch\wsds.exe tv.dis"]  # Example “off” command


# ---- MQTT Callbacks ----
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker.")
        # Subscribe to the set topic
        client.subscribe(COMMAND_TOPIC)
        # Publish discovery configuration for Home Assistant
        publish_discovery_config(client)
        # Publish default state as OFF
        client.publish(STATE_TOPIC, "OFF", retain=True)
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, msg):
    payload = msg.payload.decode().upper()
    print(f"Received command: {payload}")
    if payload == "ON":
        subprocess.Popen(COMMAND_ON)
        client.publish(STATE_TOPIC, "ON", retain=True)
    elif payload == "OFF":
        try:
            subprocess.Popen(COMMAND_OFF)
            client.publish(STATE_TOPIC, "OFF", retain=True)
        except Exception as e:
            print(f"Error executing OFF command: {e}")


def publish_discovery_config(client):
    payload = {
        "name": "Windows PC Command",
        "uniq_id": UNIQUE_ID,
        "command_topic": COMMAND_TOPIC,
        "state_topic": STATE_TOPIC,
        "payload_on": "ON",
        "payload_off": "OFF",
        "qos": 0,
        "retain": True,
    }
    topic = f"{HA_DISCOVERY_PREFIX}/switch/{SWITCH_NAME}/config"
    client.publish(topic, json.dumps(payload), retain=True)
    print(f"Published discovery configuration: {topic}")


# ---- Setup MQTT client ----
client = mqtt.Client(client_id=CLIENT_ID)

# Add username and password here
client.username_pw_set(USERNAME, PASSWORD)

# Attach the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Shutting down...")