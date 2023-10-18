from mqtt.utils.extract_info import extract_info
import requests

url = "http://127.0.0.1:8000/box/upsert"


def handle_inbound(data, collection):
    for rfid_item in data["RFID"]:
        product = extract_info(
            product_id=f"VS.{rfid_item['COMPANY']}.{rfid_item['PRODUCT']}"
        ) | {
            "zone": data["Location"],
            "box": "B-{}".format(data["Location"].split("-")[2]),
        }
        print(product)
        response = requests.post(url, json=product)
        if response.status_code == 200:
            print("Request successful")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}")

    print("Documents Updated/ Inserted")
    return {"message": "Documents Updated/ Inserted", "topic": "Inbound"}
