from fastapi import APIRouter, Body, Query, HTTPException
from models.box import Box

router = APIRouter()


@router.post("/upsert")
async def upsert(box: Box = Body(...)):
    existing_box = await Box.find_one(
        Box.company == box.company and Box.product_id == box.product_id
    )

    if existing_box:
        if box.deck:
            existing_box.deck = box.deck
        if box.area:
            existing_box.area = box.area
        if box.zone:
            existing_box.zone = box.zone
        if box.level:
            existing_box.level = box.level
        if box.box:
            existing_box.box = box.box
        if box.side:
            existing_box.side = box.side
        if box.epc:
            existing_box.epc = box.epc
        await existing_box.save()
        return box

    return await Box(**box.dict()).create()


@router.get("/fetch_one")
async def fetch_one(
    company: str = Query(..., description="Company name"),
    product_id: str = Query(..., description="Product ID"),
):
    box = await Box.find_one(Box.company == company and Box.product_id == product_id)

    if box:
        return {"message": "Box found", "box": box.dict()}
    else:
        raise HTTPException(status_code=404, detail="Box not found")


@router.get("/fetch_boxes_from_zone")
async def fetch_boxes_from_zone(zone: str = Query(..., description="Zone name")):
    boxes_in_zone = await Box.find(Box.zone == zone).to_list()

    if boxes_in_zone:
        return {
            "message": f"Boxes in zone '{zone}'",
            "boxes": [box.dict() for box in boxes_in_zone],
        }
    else:
        raise HTTPException(status_code=404, detail=f"No boxes found in zone '{zone}'")


@router.put("/update_rob")
async def update_rob(
    company: str = Query(..., description="Company name"),
    product_id: str = Query(..., description="Product ID"),
    new_rob: float = Body(..., description="new rob value"),
):
    box = await Box.find_one(Box.company == company and Box.product_id == product_id)

    if box:
        box.rob = new_rob
        await box.save()

        return {"message": f"'rob' parameter updated for the box", "box": box.dict()}
    else:
        raise HTTPException(status_code=404, detail="Box not found")
