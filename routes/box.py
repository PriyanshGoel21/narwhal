from fastapi import APIRouter, Body

from models.box import Box

router = APIRouter()


@router.post("/create")
async def create(box: Box = Body(...)):
    return await box.create()
