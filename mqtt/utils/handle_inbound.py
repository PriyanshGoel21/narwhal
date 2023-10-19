from mqtt.utils.extract_info import extract_info
import requests

url = (
    "http://127.0.0.1:8000/box/upsert"  # Define the URL for making an HTTP POST request
)


# Define a function for handling inbound data
def handle_inbound(data, collection):
    for rfid_item in data["RFID"]:
        # Create a product dictionary by extracting information from the RFID data
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

        # Make an HTTP POST request to the specified URL with the product data in JSON format
        response = requests.post(url, json=product)

        if response.status_code == 200:
            print("Request successful")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}")

    print("Documents Updated/Inserted")

    # Return a message and topic as a dictionary
    return {"message": "Documents Updated/Inserted", "topic": "Inbound"}
