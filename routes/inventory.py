from fastapi import APIRouter, Query, HTTPException

from models.product import Box, MaterialQuantity

router = APIRouter()  # Create an instance of an APIRouter


@router.get(
    "/get_quantity"
)  # Define a route for HTTP GET requests at the endpoint "/get_quantity"
async def get_quantity(
    material_desc: str = Query(..., description="Part Name")
) -> MaterialQuantity:
    """
    Handle the HTTP GET request for calculating the quantity of a specific material.

    Args:
        material_desc (str): The description of the material (Part Name).

    Returns:
        MaterialQuantity: An instance of the MaterialQuantity class.

    This function retrieves materials with a matching description and calculates the
    total quantity of the material, then returns it as a MaterialQuantity object.
    """
    materials = await Box.find(Box.material_desc == material_desc).to_list()
    # Find materials in the database with a matching 'material_desc'

    if materials:  # Check if any materials were found
        quantity = 0  # Initialize the quantity to zero
        for material in materials:  # Iterate through the found materials
            quantity += material.rob  # Accumulate the quantity of each material
        material_quantity = MaterialQuantity(
            material_desc=material_desc, quantity=quantity
        )
        # Create a MaterialQuantity instance with the calculated quantity
        return material_quantity  # Return the MaterialQuantity instance
    else:
        raise HTTPException(status_code=404, detail="Material not found")
        # Raise an HTTPException with a 404 status code if no materials were found


# This code defines a FastAPI route that calculates the quantity of a specific material
# based on its description (Part Name) and returns it in a MaterialQuantity object.
