import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI
import routes.box
import routes.inventory
from models.box import Box

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017",
)

db = client.narwhal_tof


@app.on_event("startup")
async def start_database():
    await init_beanie(database=db, document_models=[Box])


@app.get("/")
def home():
    return {"Hello"}


app.include_router(routes.box.router, tags=["Boxes"], prefix="/box")
app.include_router(routes.inventory.router, tags=["Inventory"], prefix="/inventory")
