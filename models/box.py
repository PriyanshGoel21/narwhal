from enum import Enum
from typing import Optional, List
from beanie import Document, BackLink, Link
from pydantic import Field
from models.machine import Machine
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
    area: Area
    zone: int
    level: int
    side: Side
    type: Type
    machine: BackLink[Machine] = Field(original_field="boxes")
    products: Optional[List[Link[Product]]]
