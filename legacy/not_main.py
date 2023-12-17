import motor.motor_asyncio
from beanie import init_beanie
from fastapi.middleware.cors import CORSMiddleware

import legacy.routes.inventory
import legacy.routes.pms
from legacy.models.jobs import Job
from legacy.models.product import Product

# Create a FastAPI application instance

# app = FastAPI()

origins = [
    "http://localhost:3000",
]

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
    "mongodb://root:example2@139.59.59.166:27017/"
)

# Access the 'narwhal_tof' database using the client
db = client.narwhal_tof


# Initialize Beanie for async document modeling and interaction with the MongoDB database
@app.on_event("startup")
async def start_database():
    await init_beanie(database=db, document_models=[Product, Job])


# Define a route at the root endpoint
@app.get("/")
def home():
    return {"Hello, World! "}


# Include route handlers for the "box" and "inventory" related endpoints
app.include_router(legacy.routes.product.router, tags=["products"], prefix="/products")
app.include_router(
    legacy.routes.inventory.router, tags=["Inventory"], prefix="/inventory"
)
app.include_router(legacy.routes.pms.router, tags=["PMS"], prefix="/pms")
