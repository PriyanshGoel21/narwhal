import csv

file_path = "/Users/naad/PycharmProjects/narwhal/mqtt/temp_data/HHDG - SpareInventory.xlsx - HHDG - SpareInventory.csv"


def extract_info(product_id):
    with open(file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            match = row["MATERIAL"]

            if product_id == match:
                matched_item = {
                    "PRODUCT": product_id,
                    "MACH_DESC": row["MACH_DESC"],
                    "MAKER_DESC": row["MAKER_DESC"],
                    "MATERIAL": row["MATERIAL"],
                    "MATERIAL_DESC": row["MATERIAL_DESC"],
                    "PART_NO": row["PART_NO"],
                    "ROB": row["ROB"],
                }
                return matched_item

    matched_item = {
        "PRODUCT": product_id,
        "MACH_DESC": "unavailable",
        "MAKER_DESC": "unavailable",
        "MATERIAL": "unavailable",
        "MATERIAL_DESC": "unavailable",
        "PART_NO": "unavailable",
        "ROB": "unavailable",
    }
    return matched_item
