import os
import asyncio
import motor.motor_asyncio
from beanie import init_beanie
from models.box import Box, Area
from datetime import date


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("DATABASE_URL"))
today = date.today()
db = client.narwhal


async def update_jobs_status():
    await init_beanie(database=db, document_models=[Box])

    await Box.update_all({}, {"$set": {"room": ""}})
    print("ok")


async def update_boxes():
    await init_beanie(database=db, document_models=[Box])

    # area_to_room_mapping = {Area.A: Area.MAIN_INVENTORY, Area.B: Area.PURIFIER, Area.C: Area.ENGINE_CONTROL}

    all_entries = await Box.find().to_list()
    print(all_entries)

    # for entry in all_entries:
    #     area_value = entry.area
    #     room_value = area_to_room_mapping.get(area_value, Area.MAIN_INVENTORY)
    #     entry.area = room_value
    #
    # await Box.replace_many(all_entries)

    print("ok")


# asyncio.run(update_jobs_status())
asyncio.run(update_boxes())
# x = await update_boxes()