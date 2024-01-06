import os
import asyncio
import random

import motor.motor_asyncio
from beanie import init_beanie
from models.box import Box, Room
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


async def add_shelves_and_racks():
    await init_beanie(database=db, document_models=[Box])

    all_entries = await Box.find().to_list()

    r = len(all_entries) // 36
    s = r // 6

    for i, entry in enumerate(all_entries):
        entry.rack = (i % r) // s + 1
        entry.shelf = (i % s) + 1

    await Box.replace_many(all_entries)
    print("Shelves and racks added/updated")


async def update_field_name():
    await init_beanie(database=db, document_models=[Box])

    await Box.update_all({}, {"$rename": {"zone": "rack"}})
    await Box.update_all({}, {"$rename": {"level": "shelf"}})

    print("Field name updated")


# asyncio.run(update_jobs_status())
asyncio.run(add_shelves_and_racks())
