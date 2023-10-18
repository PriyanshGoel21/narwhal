from fastapi import APIRouter, Body

from models.box import Box, UpdateBox

router = APIRouter()


@router.post("/create")
async def create(box: Box = Body(...)):
    return await box.create()


@router.post("/update")
async def update(update_box: UpdateBox = Body(...)):
    box = await Box.find_one(
        Box.company == update_box.company and Box.product_id == update_box.product_id
    )
    if update_box.deck:
        box.deck = update_box.deck
    if update_box.area:
        box.area = update_box.area
    if update_box.zone:
        box.zone = update_box.zone
    if update_box.level:
        box.level = update_box.level
    if update_box.box:
        box.box = update_box.box
    if update_box.side:
        box.side = update_box.side
    if update_box.epc:
        box.epc = update_box.epc
    await box.save()

