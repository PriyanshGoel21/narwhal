from typing import List

from beanie import WriteRules
from fastapi import APIRouter, Body, HTTPException

from models.box import Box, CreateBox
from models.product import Product

router = APIRouter()


@router.post("/create_box")
async def create_box(box: CreateBox = Body(...)) -> Box:
    exists = await Box.find(box.model_dump(exclude={"machine_name"})).to_list()
    if exists:
        raise HTTPException(status_code=403, detail="Box already exists")
    box = Box(
        level=box.level,
        side=box.side,
        type=box.type,
        zone=box.zone,
        area=box.area,
        machine_name=box.machine_name,
        deck=box.deck,
        products=[],
    )
    box = await box.insert()
    return box


@router.post("/add_products")
async def add_products(box_id: str, products: List[Product]) -> Box:
    exists = await Box.get(box_id, fetch_links=True)
    if not exists:
        raise HTTPException(status_code=404, detail="Box not found")
    for product in products:
        product = await product.insert()
        exists.products.append(product)
    await exists.save(link_rule=WriteRules.WRITE)
    return exists


@router.post("/get_products")
async def get_products(box_id: str) -> Box:
    exists = await Box.get(box_id, fetch_links=True)
    if not exists:
        raise HTTPException(status_code=404, detail="Box not found")
    return exists
