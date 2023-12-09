import time

import requests
import json
import random

url = 'http://139.59.59.166/products/upsert'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

decks = [deck for deck in range(1, 4)]
areas = ["A", "B", "C"]
zones = [zone for zone in range(1, 6)]
levels = [level for level in range(1, 4)]
boxes = [box for box in range(1, 13)]
sides = ["front", "rear"]
types = ["metal", "cardboard"]
mach_desc = list()
maker_desc = list()
company = ["CAS", "BWS", "SGS", "FOS", "LOS", "SHS", "WOS", "MES", "GES", "ACR", "FWS", "STS", "HMC", "AUS", "NAS", "POE"]
material_desc = list()

with open("mach_desc", "r") as file:
    mach_desc = file.read().split("\n")

for mach in mach_desc:
    if mach == " ":
        mach_desc.remove(mach)
    else: mach = mach[-2]

with open("maker_desc", "r") as file:
    maker_desc = file.read().split("\n")

for mach in maker_desc:
    if mach == " ":
        maker_desc.remove(mach)
    else: mach = mach[-2]

with open("material_desc", "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        try:
            material_desc.append(line)
        except Exception as e:
            pass

for mach in material_desc:
    if mach == " ":
        material_desc.remove(mach)
    else: mach = mach[-2]

def populate_db():
    product_id = 0
    for deck in decks:
        for area in areas:
            for zone in zones:
                for level in levels:
                    for box in range(1, random.randint(5, 14)):
                        for side in sides:
                            for i in range(random.randint(0, 10)):
                                com = random.choice(company)
                                data = {
                                    "product_id": str(product_id),
                                    "company": com,
                                    "deck": deck,
                                    "area": area,
                                    "zone": zone,
                                    "level": level,
                                    "box": box,
                                    "side": side,
                                    "type": random.choice(types),
                                    "epc": f"{20000 - product_id}",
                                    "mach_desc": random.choice(mach_desc),
                                    "maker_desc": random.choice(maker_desc),
                                    "material_desc": f"VS.{com}.{product_id}",
                                    "material_desc": random.choice(material_desc)[:-2],
                                    "part_no": str(product_id),
                                    "rob": random.randint(1, 10)
                                }

                                response = requests.post(url, headers=headers, data=json.dumps(data))

                                print(response.json())
                                product_id += 1

populate_db()


#
# import time
# import requests
# import json
# import random
# from concurrent.futures import ThreadPoolExecutor
#
# url = 'http://139.59.59.166/products/upsert'
# headers = {
#     'accept': 'application/json',
#     'Content-Type': 'application/json'
# }
#
# decks = [deck for deck in range(1, 4)]
# areas = ["A", "B", "C"]
# zones = [zone for zone in range(1, 6)]
# levels = [level for level in range(1, 4)]
# boxes = [box for box in range(1, 13)]
# sides = ["front", "rear"]
# types = ["metal", "cardboard"]
#
# def post_data(product_id, deck, area, zone, level, box, side, type):
#     data = {
#         "product_id": str(product_id),
#         "company": "string",
#         "deck": deck,
#         "area": area,
#         "zone": zone,
#         "level": level,
#         "box": box,
#         "side": side,
#         "type": type,
#         "epc": "string",
#         "mach_desc": "string",
#         "maker_desc": "string",
#         "material_desc": "string",
#         "material_desc": "string",
#         "part_no": "string",
#         "rob": random.randint(1, 10)
#     }
#
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     print(response.json())
#
# def populate_db():
#     product_id = 0
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         for deck in decks:
#             for area in areas:
#                 for zone in zones:
#                     for level in levels:
#                         for box in boxes:
#                             for side in sides:
#                                 for type in types:
#                                     executor.submit(post_data, product_id, deck, area, zone, level, box, side, type)
#                                     product_id += 1
#
# populate_db()
