from utils.extract_info import extract_info

def handle_inbound(data, collection):
    for rfid_item in data["RFID"]:
        product = rfid_item | extract_info(product_id=f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}") | {
            "Zone": data["Location"],
            "Box": "B-{}".format(data["Location"].split("-")[2]),
            "ZONE": int(data["Location"].split("-")[0].replace("Zone", "")),
            "LEVEL": int(data["Location"].split("-")[1]),
            "BOX": data["Location"].split("-")[2],
        }

        product_id_filter = {"PRODUCT": f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}"}
        collection.update_one(product_id_filter, {"$set": product}, upsert=True)
    print("Documents Updated/ Inserted")
    return {'message': "Documents Updated/ Inserted", "topic": "Inbound"}
