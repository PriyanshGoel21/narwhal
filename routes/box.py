from typing import List
from fastapi import (
    APIRouter,
    Body,
    Query,
    HTTPException,
)
from models.box import (
    Box,
    UpdateROB,
)

router = APIRouter()  # Create an instance of an APIRouter


@router.post(
    "/upsert"
)  # Define a route for HTTP POST requests at the endpoint "/upsert"
async def upsert(box: Box = Body(...)):
    """
    Handle the HTTP POST request to upsert (update or insert) a Box.

    Args:
        box (Box): The Box instance to upsert.

    Returns:
        Box: The updated or inserted Box instance.

    This function checks if a Box with the same company and product_id exists. If it
    does, it updates the existing Box; otherwise, it inserts a new Box.
    """
    existing_box = await Box.find_one(
        Box.company == box.company and Box.product_id == box.product_id
    )

    if existing_box:  # Check if a Box with the same company and product_id exists
        # Update the existing Box with the values from the provided 'box'
        existing_box.deck = box.deck
        existing_box.area = box.area
        existing_box.zone = box.zone
        existing_box.level = box.level
        existing_box.box = box.box
        existing_box.side = box.side
        existing_box.epc = box.epc
        await existing_box.save()  # Save the updated Box
        return box  # Return the updated Box
    else:
        # If no existing Box is found, insert a new Box based on the provided 'box'
        return await Box(**box.dict()).create()


@router.get(
    "/fetch_one"
)  # Define a route for HTTP GET requests at the endpoint "/fetch_one"
async def fetch_one(
    company: str = Query(..., description="Company name"),
    product_id: str = Query(..., description="Product ID"),
) -> Box:
    """
    Handle the HTTP GET request to fetch one Box based on company and product_id.

    Args:
        company (str): The company name.
        product_id (str): The product ID.

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
