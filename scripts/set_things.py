import os
import asyncio
import motor.motor_asyncio
from beanie import init_beanie
from models.jobs import Job
from datetime import date


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("DATABASE_URL"))
today = date.today()
db = client.narwhal


async def update_jobs_status():
    await init_beanie(database=db, document_models=[Job])

    await Job.update_all({}, {"$set": {"due_date": ""}})
    print("ok")


asyncio.run(update_jobs_status())
