from mqtt.utils.extract_info import extract_info
import requests

url = "http://127.0.0.1:8000/box/upsert"


def handle_inbound(data, collection):
    for rfid_item in data["RFID"]:
        product = {
            "product_id": rfid_item["PRODUCT"],
            "company": rfid_item["COMPANY"],
            "deck": data["Deck"],
            "area": data["Area"],
            "zone": int(data["Location"].split("-")[0][4:]),
            "level": int(data["Location"].split("-")[1]),
            "box": int(data["Location"].split("-")[2]),
            "side": data["SIDE"],
            "epc": rfid_item["EPC"],
        } | extract_info(product_id=f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}")
        print(product)
        response = requests.post(url, json=product)
        if response.status_code == 200:
            print("Request successful")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}")

    print("Documents Updated/ Inserted")
    return {"message": "Documents Updated/ Inserted", "topic": "Inbound"}
