from enum import Enum

from beanie import Document
from pydantic import BaseModel


# Define an enumeration for 'Side'
class Side(str, Enum):
    front = "front"
    back = "rear"


# Define an enumeration for 'Area'
class Area(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


# Define a Beanie Document class for 'Box'
class Product(Document):
    product_id: str
    company: str
    deck: int
    area: Area
    zone: int
    level: int
    box: int
    side: Side
    epc: str
    mach_desc: str
    maker_desc: str
    material: str
    material_desc: str
    part_no: str
    rob: int


# Define a Pydantic BaseModel for 'UpdateROB'
class UpdateROB(BaseModel):
    company: str
    product_id: str
    rob: int


# Define a Pydantic BaseModel for 'MaterialQuantity'
class MaterialQuantity(BaseModel):
    material_desc: str
    quantity: int


class Box(BaseModel):
    deck: int
    area: Area
    zone: int
    level: int
    box: int
    side: Side
