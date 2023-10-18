import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
import sys
import locale
from utils.handle_inbound import handle_inbound
from utils.handle_outbound import handle_outbound

new_locale = "en_US.UTF-8"
locale.setlocale(locale.LC_ALL, new_locale)

db_client = MongoClient("mongodb://localhost:27017")
db = db_client["Product_Management"]
collection = db["products"]


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker\nlistening for info on ...")
        client.subscribe("Inbound")
        print("Subscribed to 'Inbound' topic")
        client.subscribe("Outbound")
        print("Subscribed to 'Outbound' topic")
    else:
        print("Connection failed")


def on_message(client, userdata, message):
    print(sys.getdefaultencoding())
    print(message.payload)
    print("UserData: {}".format(userdata))
    print("Client: {}".format(client))

    payload = message.payload.decode("utf-8")
    data = json.loads(payload)

    if message.topic == "Inbound":
        out = handle_inbound(data=data, collection=collection)
    if message.topic == "Outbound":
        out = handle_outbound(data=data, collection=collection)
    else:
        out = {"message": "No message yet on subscribed topics"}


mqttBroker = "localhost"

client = mqtt.Client("RFID", clean_session=False)
print("MQTT Broker: {}".format(mqttBroker))
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqttBroker, 1884)

client.loop_forever()
