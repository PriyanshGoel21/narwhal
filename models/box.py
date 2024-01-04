from enum import Enum
from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel

from models.product import Product


class Type(str, Enum):
    metal = "metal"
    cardboard = "cardboard"


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


class Box(Document):
    deck: int
    area: Area
    zone: int
    level: int
    side: Side
    type: Type
    machine_name: str
    products: Optional[List[Link[Product]]]


class CreateBox(BaseModel):
    deck: int
    area: Area
    zone: int
    level: int
    side: Side
    type: Type
    machine_name: str
