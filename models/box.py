from enum import Enum
from beanie import Document
from pydantic import BaseModel


class Side(str, Enum):
    front = "front"
    back = "rear"


class Area(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Box(Document):
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


class UpdateROB(BaseModel):
    company: str
    product_id: str
    rob: int


class MaterialQuantity(BaseModel):
    material_desc: str
    quantity: int
