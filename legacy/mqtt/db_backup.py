import urllib.request
from pymongo import MongoClient
import datetime
from pytz import timezone
from time import sleep
import certifi as certifi

# Local Database
db_client = MongoClient(
    "mongodb://127.0.0.1:27017/"
)  # Connect to the local MongoDB server
db = db_client["narwahal_tof"]  # Select the 'narwahal_tof' database
collection = db["Box"]  # Select the 'Box' collection within the database

# Deployed Database for Backup
db_client2 = MongoClient(
    "mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/",
    tlsCAFile=certifi.where(),
)
db_console = db_client2["narwahal_tof"]
collection_products = db_console["Box"]


# Define a function to check internet connectivity
def connect():
    try:
        urllib.request.urlopen("http://google.com/")
        return True
    except:
        return False


# Define a function to backup collections from the local database to the deployed database
def backup_collections():
    for product in collection.find():
        product_id_filter = {
            "product_id": product["product_id"],
            "company": product["company"],
        }
        collection_products.update_one(
            product_id_filter, {"$set": product}, upsert=True
        )
        print("Backup completed")

    timestamp = datetime.datetime.now(timezone("Asia/Kolkata"))
    print(f"Backup completed at {timestamp}")


# Continuously attempt to back up collections
while True:
    try:
        if connect():
            print("Connection established")
            backup_collections()
            sleep(11)  # Successful backups will occur at longer intervals
        else:
            print("No internet connection")
            sleep(
                10
            )  # Connection will be checked more frequently in case of no internet connection

    except KeyboardInterrupt:
        print("Ended")
        break  # Exit the loop if a KeyboardInterrupt is received
