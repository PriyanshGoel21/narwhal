import motor.motor_asyncio
from beanie import init_beanie
from fastapi import FastAPI
import routes.box
import routes.inventory
from models.box import Box
from fastapi.middleware.cors import CORSMiddleware


# Create a FastAPI application instance

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up an AsyncIOMotorClient for connecting to MongoDB
# client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://narwahal:narwahal%40123@139.59.59.166:27017/"
)

# Access the 'narwhal_tof' database using the client
db = client.narwhal_tof


# Initialize Beanie for async document modeling and interaction with the MongoDB database
@app.on_event("startup")
async def start_database():
    await init_beanie(database=db, document_models=[Box])


# Define a route at the root endpoint
@app.get("/")
def home():
    return {"Hello"}


# Include route handlers for the "box" and "inventory" related endpoints
app.include_router(routes.box.router, tags=["Boxes"], prefix="/box")
app.include_router(routes.inventory.router, tags=["Inventory"], prefix="/inventory")
