from collections import OrderedDict
from typing import List

from fastapi import (
    APIRouter,
    Body,
    Query,
    HTTPException,
)

from models.product import (
    Product,
    UpdateROB,
    Box,
)

router = APIRouter()  # Create an instance of an APIRouter


@router.post(
    "/upsert"
)  # Define a route for HTTP POST requests at the endpoint "/upsert"
async def upsert(product: Product = Body(...)):
    """
    Handle the HTTP POST request to upsert (update or insert) a product.

    Args:
        product (Product): The Box instance to upsert.

    Returns:
        Product: The updated or inserted Product instance.

    This function checks if a Box with the same company and product_id exists. If it
    does, it updates the existing Box; otherwise, it inserts a new Box.
    """
    existing_box = await Product.find_one(
        Product.company == product.company and Product.product_id == product.product_id
    )

    if existing_box:  # Check if a Box with the same company and product_id exists
        # Update the existing Box with the values from the provided 'box'
        existing_box.deck = product.deck
        existing_box.area = product.area
        existing_box.zone = product.zone
        existing_box.level = product.level
        existing_box.box = product.box
        existing_box.type = product.type
        existing_box.side = product.side
        existing_box.epc = product.epc
        await existing_box.save()  # Save the updated Box
        return product  # Return the updated Box
    else:
        # If no existing Box is found, insert a new Box based on the provided 'box'
        return await Product(**product.dict()).create()


@router.get(
    "/fetch_product"
)  # Define a route for HTTP GET requests at the endpoint "/fetch_one"
async def fetch_one(
    company: str = Query(..., description="Company name"),
    product_id: str = Query(..., description="Product ID"),
) -> Product:
    """
    Handle the HTTP GET request to fetch one Box based on company and product_id.

    Args:
        company (str): The company name.
        product_id (str): The product ID.

    Returns:
        Box: The fetched Box instance.

    This function retrieves a Box with a matching company and product_id and returns it.
    """
    product = await Product.find_one(
        Product.company == company and Product.product_id == product_id
    )

    if product:  # Check if a Box was found
        return product  # Return the fetched Box
    else:
        raise HTTPException(
            status_code=404, detail="Product not found"
        )  # Raise a 404 error if no Box is found


@router.get("/fetch_products")
async def fetch_products(
    deck: int = Query(..., description="Deck"),
    area: str = Query(..., description="Area"),
    zone: int = Query(..., description="Zone"),
    side: str = Query(..., description="Side"),
    level: int = Query(..., description="Level"),
    box: int = Query(..., description="Box"),
) -> list[Product]:
    products_in_zone = await Product.find(
        Product.deck == deck
        and Product.area == area
        and Product.zone == zone
        and Product.side == side
        and Product.box == box
        and Product.level == level
    ).to_list()
    if products_in_zone:  # Check if any boxes were found in the specified zone
        return [product for product in products_in_zone]  # Return the list of boxes
    else:
        raise HTTPException(status_code=404, detail=f"No products found")


@router.get(
    "/fetch_boxes"
)  # Define a route for HTTP GET requests at the endpoint "/fetch_boxes_from_zone"
async def fetch_boxes_from_zone(
    deck: int = Query(..., description="Deck"),
    area: str = Query(..., description="Area"),
    zone: int = Query(..., description="Zone"),
) -> List[Box]:
    """
    Handle the HTTP GET request to fetch boxes from a specific zone.

    Args:
        deck (int): The deck number.
        area (str): The area name.
        zone (int): The zone number.

    Returns:
        List[Box]: A list of Box instances in the specified zone.

    This function retrieves a list of Box instances that match the specified deck, area,
    and zone.
    """
    boxes_in_zone = (
        await Product.find(
            Product.deck == deck and Product.area == area and Product.zone == zone
        )
        .project(Box)
        .to_list()
    )

    if boxes_in_zone:  # Check if any boxes were found in the specified zone
        return list(
            OrderedDict(
                ((box.deck, box.area, box.zone, box.box), box) for box in boxes_in_zone
            ).values()
        )
    else:
        raise HTTPException(status_code=404, detail=f"No boxes found in zone '{zone}'")
        # Raise a 404 error if no boxes are found in the specified zone


@router.put(
    "/update_rob"
)  # Define a route for HTTP PUT requests at the endpoint "/update_rob"
async def update_rob(updated_box: UpdateROB = Body(...)) -> Box:
    """
    Handle the HTTP PUT request to update the remaining on board (ROB) of a Box.

    Args:
        updated_box (UpdateROB): The Box instance with updated ROB.

    Returns:
        Box: The updated Box instance.

    This function updates the ROB of a Box with the values from the provided 'updated_box'.
    """
    box = await Box.find_one(
        Box.company == updated_box.company and Box.product_id == updated_box.product_id
    )

    if box:  # Check if a Box with the same company and product_id exists
        # Update the ROB of the existing Box with the value from 'updated_box'
        box.rob = updated_box.rob
        await box.save()  # Save the updated Box
        return box  # Return the updated Box
    else:
        raise HTTPException(
            status_code=404, detail="Box not found"
        )  # Raise a 404 error if no Box is found
