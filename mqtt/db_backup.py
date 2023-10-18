import urllib.request
from pymongo import MongoClient
import datetime
from pytz import timezone
from time import sleep
import certifi as certifi

# Local Database
db_client = MongoClient("mongodb://127.0.0.1:27017/")
db = db_client["narwahal_tof"]
collection = db["Box"]

# Deployed Database for Backup
db_client2 = MongoClient(
    "mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/",
    tlsCAFile=certifi.where(),
)
db_console = db_client2["narwahal_tof"]
collection_products = db_console["Box"]


def connect():
    try:
        urllib.request.urlopen("http://google.com/")
        return True
    except:
        return False


def backup_collections():
    for product in collection.find():
        product_id_filter = {
            "product_id": product["product_id"],
            "company": product["company"],
        }
        collection_products.update_one(
            product_id_filter, {"$set": product}, upsert=True
        )
        print("ok")

    timestamp = datetime.datetime.now(timezone("Asia/Kolkata"))
    print(f"Backup completed at {timestamp}")


while True:
    try:
        if connect():
            print("connection established")
            backup_collections()
            sleep(11)  # successful backups will occur in longer intervals
        else:
            print("no internet connection")
            sleep(
                10
            )  # connection will be checked more frequently in case of no internet connection

    except KeyboardInterrupt:
        print("Ended")
        break
