import os

import motor.motor_asyncio
import uvicorn
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get("DATABASE_URL"))

db = client.narwhal


@app.on_event("startup")
async def start_database():
    await init_beanie(database=db, document_models=[])


@app.get("/")
async def home():
    return JSONResponse("home")


# app.include_router(routes.product.router, tags=["products"], prefix="/products")

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=81, reload=True)
