
from fastapi import APIRouter, Query, HTTPException
from models.product import Product, MaterialQuantity
router = APIRouter()


# async def get_quantity_of_material(
#     material_code: str
# ) -> MaterialQuantity | None:
#     materials = await Product.find(Product.product_id == material_code).to_list()
#     # Find materials in the database with a matching 'material_desc'
#
#     if materials:  # Check if any materials were found
#         quantity = 0  # Initialize the quantity to zero
#         for material in materials:  # Iterate through the found materials
#             quantity += material.rob  # Accumulate the quantity of each material_desc
#         # Create a MaterialQuantity instance with the calculated quantity
#         return MaterialQuantity(
#             material_desc=material_desc, quantity=quantity
#         )  # Return the MaterialQuantity instance
#     else:
#         return MaterialQuantity(
#             material_desc=material_desc, quantity=0
#         )


@router.get(
    "/get_quantity"
)  # Define a route for HTTP GET requests at the endpoint "/get_quantity"
async def get_quantity(
    material_desc: str = Query(..., description="Part Name")
) -> MaterialQuantity:
    """
    Handle the HTTP GET request for calculating the quantity of a specific material_desc.
    
    Args:
        material_desc (str): The description of the material_desc (Part Name).

    Returns:
        MaterialQuantity: An instance of the MaterialQuantity class.

    This function retrieves materials with a matching description and calculates the
    total quantity of the material_desc, then returns it as a MaterialQuantity object.
    """
    material_qty = await get_quantity_of_material(material_desc=material_desc)

    if material_qty is not None:  # Check if any materials were found
        return material_qty
    else:
        raise HTTPException(status_code=404, detail="Material not found")
        # Raise an HTTPException with a 404 status code if no materials were found


# This code defines a FastAPI route that calculates the quantity of a specific material_desc
# based on its description (Part Name) and returns it in a MaterialQuantity object.
