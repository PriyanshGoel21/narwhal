import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import sys
import locale
from utils.handle_inbound import handle_inbound
from utils.handle_outbound import handle_outbound

# Set the new locale for localization settings
new_locale = "en_US.UTF-8"
locale.setlocale(locale.LC_ALL, new_locale)

# Connect to the MongoDB server running locally
db_client = MongoClient("mongodb://localhost:27017")
db = db_client["narwahal_tof"]
collection = db["products"]


# Define the function to be executed when the MQTT client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\nlistening for info on ...")
        client.subscribe("Inbound")
        print("Subscribed to 'Inbound' topic")
        client.subscribe("Outbound")
        print("Subscribed to 'Outbound' topic")
    else:
        print("Connection failed")


# Define the function to be executed when the MQTT client receives a message
def on_message(client, userdata, message):
    print(sys.getdefaultencoding())
    print(message.payload)
    print("UserData: {}".format(userdata))
    print("Client: {}".format(client))

    # Decode the message payload from bytes to a UTF-8 string
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)  # Parse the JSON data from the payload

    if message.topic == "Inbound":
        out = handle_inbound(data=data, collection=collection)
    if message.topic == "Outbound":
        out = handle_outbound(data=data, collection=collection)
    else:
        out = {"message": "No message yet on subscribed topics"}


# Define the MQTT broker's address
mqttBroker = "localhost"

# Create an MQTT client instance named "RFID" with a persistent session
client = mqtt.Client("RFID", clean_session=False)
print("MQTT Broker: {}".format(mqttBroker))

# Set the on_connect and on_message callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker at the specified address and port (1884)
client.connect(mqttBroker, 1884)

# Start the MQTT client's main loop to handle communication with the broker
client.loop_forever()
