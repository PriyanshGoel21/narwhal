from typing import List

from fastapi import APIRouter, Body, Query, HTTPException
from models.box import Box, FetchBoxesFromZone, UpdateROB

router = APIRouter()


@router.post("/upsert")
async def upsert(box: Box = Body(...)):
    existing_box = await Box.find_one(
        Box.company == box.company and Box.product_id == box.product_id
    )

    if existing_box:
        existing_box.deck = box.deck
        existing_box.area = box.area
        existing_box.zone = box.zone
        existing_box.level = box.level
        existing_box.box = box.box
        existing_box.side = box.side
        existing_box.epc = box.epc
        await existing_box.save()
        return box

    return await Box(**box.dict()).create()


@router.get("/fetch_one")
async def fetch_one(
    company: str = Query(..., description="Company name"),
    product_id: str = Query(..., description="Product ID"),
) -> Box:
    box = await Box.find_one(Box.company == company and Box.product_id == product_id)

    if box:
        return box
    else:
        raise HTTPException(status_code=404, detail="Box not found")


@router.get("/fetch_boxes_from_zone")
async def fetch_boxes_from_zone(
    deck: int = Query(..., description="Deck"),
    area: str = Query(..., description="Area"),
    zone: int = Query(..., description="Zone"),
) -> List[Box]:
    boxes_in_zone = await Box.find(
        Box.deck == deck and Box.area == area and Box.zone == zone
    ).to_list()

    if boxes_in_zone:
        return [box for box in boxes_in_zone]
    else:
        raise HTTPException(status_code=404, detail=f"No boxes found in zone '{zone}'")


@router.put("/update_rob")
async def update_rob(updated_box: UpdateROB = Body(...)) -> Box:
    box = await Box.find_one(
        Box.company == updated_box.company and Box.product_id == updated_box.product_id
    )

    if box:
        box.rob = updated_box.rob
        await box.save()
        return box
    else:
        raise HTTPException(status_code=404, detail="Box not found")
