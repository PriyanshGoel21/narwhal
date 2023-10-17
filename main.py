import certifi
import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI

import routes.box
from models.box import Box

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://Naad:naad2002@cluster0.7redvzp.mongodb.net/",
    tlsCAfile=certifi.where(),
)

db = client.narwhal_tof


@app.on_event("startup")
async def start_database():
    await init_beanie(database=db, document_models=[Box])


app.include_router(routes.box.router, tags=["Boxes"], prefix="/box")
