import motor.motor_asyncio

mongo_client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = mongo_client.narwhal_tof


async def extract_info(product_id):
    collection = db.product_info
    document = await collection.find_one({"MATERIAL": product_id})

    if document:
        matched_item = {
            "mach_desc": document.get("MACH_DESC", "unavailable"),
            "maker_desc": document.get("MAKER_DESC", "unavailable"),
            "material": document.get("MATERIAL", "unavailable"),
            "material_desc": document.get("MATERIAL_DESC", "unavailable"),
            "part_no": document.get("PART_NO", "unavailable"),
            "rob": document.get("ROB", "unavailable"),
        }
    else:
        matched_item = {}

    return matched_item
