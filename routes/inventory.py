from fastapi import APIRouter, Body, Query, HTTPException
from models.box import Box, MaterialQuantity

router = APIRouter()


@router.get("/get_quantity")
async def get_quantity(
    material_desc: str = Query(..., description="Part Name")
) -> MaterialQuantity:
    materials = await Box.find(Box.material_desc == material_desc).to_list()
    if materials:
        quantity = 0
        for material in materials:
            quantity += material.rob
        material_quantity = MaterialQuantity(
            material_desc=material_desc, quantity=quantity
        )
        return material_quantity
    else:
        raise HTTPException(status_code=404, detail="Material not found")
