from typing import List

from beanie import WriteRules
from beanie.odm.operators.find.evaluation import RegEx
from beanie.odm.operators.find.logical import Or
from fastapi import APIRouter, Body, HTTPException, Query

from models.box import Box, CreateBox
from models.product import Product

router = APIRouter()


@router.post("/create_box")
async def create_box(box: CreateBox = Body(...)) -> Box:
    exists = await Box.find(box.model_dump(exclude={"machine_name"})).to_list()
    if exists:
        raise HTTPException(status_code=403, detail="Box already exists")
    box = Box(
        deck=box.deck,
        room=box.room,
        machine_name=box.machine_name,
        products=[],
        shelf=box.shelf,
        rack=box.rack,
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


@router.get("/get_products")
async def get_products(box_id: str) -> Box:
    exists = await Box.get(box_id, fetch_links=True)
    if not exists:
        raise HTTPException(status_code=404, detail="Box not found")
    return exists


@router.get("/fetch_boxes")
async def fetch_boxes_from_zone(
    deck: int = Query(..., description="Deck"),
    rack: int = Query(..., description="Rack"),
    shelf: int = Query(..., description="Shelf"),
    room: str = Query(..., description="Room"),
) -> List[Box]:
    boxes = await Box.find(
        Box.deck == deck, Box.rack == rack, Box.shelf == shelf, Box.room == room
    ).to_list()
    return boxes


@router.put("/update_rob")
async def update_rob(product_id: str, new_rob: int) -> Product:
    exists = await Product.get(product_id)
    if exists:
        exists.rob = new_rob
        await exists.save()
        return exists
    raise HTTPException(status_code=404, detail="Product not found")


@router.get("/search_product")
async def fetch_one(
    search_string: str = Query(..., description="Company name")
) -> list[Product]:
    product = await Product.find(
        Or(
            RegEx(Product.material_code, search_string, "i"),
            RegEx(Product.material_desc, search_string, "i"),
        )
    ).to_list()
    if product:
        return product[:10]
    else:
        raise HTTPException(status_code=404, detail="Product not found")
