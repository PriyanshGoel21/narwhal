import csv

file_path = "/Users/naad/PycharmProjects/narwhal/mqtt/temp_data/HHDG - SpareInventory.xlsx - HHDG - SpareInventory.csv"


def extract_info(product_id):
    with open(file_path, mode="r") as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            match = row["MATERIAL"]

            if product_id == match:
                matched_item = {
                    "product_id": product_id.split(".")[2],
                    "mach_desc": row["MACH_DESC"],
                    "maker_desc": row["MAKER_DESC"],
                    "material": row["MATERIAL"],
                    "material_desc": row["MATERIAL_DESC"],
                    "part_no": row["PART_NO"],
                    "rob": row["ROB"],
                }
                return matched_item

    matched_item = {
        "product_id": product_id,
        "mach_desc": "unavailable",
        "maker_desc": "unavailable",
        "material": "unavailable",
        "material_desc": "unavailable",
        "part_no": "unavailable",
        "rob": "unavailable",
    }
    return matched_item
