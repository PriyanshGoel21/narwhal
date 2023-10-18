from mqtt.utils.extract_info import extract_info

def handle_outbound(data, collection):
    for rfid_item in data["RFID"]:
        product = rfid_item | extract_info(product_id=f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}") | {
            "Zone": "Zone0-0-0",
            "Box": "B-{}".format("0"),
            "ZONE": 0,
            "LEVEL": 0,
            "BOX": "0",
        }

        product_id_filter = {"PRODUCT": f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}"}
        collection.update_one(product_id_filter, {"$set": product}, upsert=True)
    print("Documents added to Zone0-0-0")
    return {'message': "Documents added to Zone0-0-0", "topic": "Outbound"}
