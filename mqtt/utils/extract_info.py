import pymongo

# mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
mongo_client = pymongo.MongoClient(
    "mongodb://narwahal:narwahal%40123@139.59.59.166:27017/"
)
db = mongo_client.narwhal_tof


# Define a function 'extract_info' that takes 'product_id' as a parameter
def extract_info(product_id):
    # Select the 'product_info' collection within the 'narwhal_tof' database
    collection = db.product_info

    # Search for a document in the collection where the "MATERIAL" field matches 'product_id'
    document = collection.find_one({"MATERIAL": product_id})

    # Check if a matching document was found
    if document:
        # If found, create a dictionary 'matched_item' with various fields, using default values if not present
        matched_item = {
            "mach_desc": document.get("MACH_DESC", "unavailable"),
            "maker_desc": document.get("MAKER_DESC", "unavailable"),
            "material": document.get("MATERIAL", "unavailable"),
            "material_desc": document.get("MATERIAL_DESC", "unavailable"),
            "part_no": document.get("PART_NO", "unavailable"),
            "rob": document.get("ROB", "unavailable"),
        }

    else:
        # If no matching document was found, set 'matched_item' as an empty dictionary
        matched_item = {}

    return matched_item
