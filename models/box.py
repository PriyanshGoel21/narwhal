from enum import Enum
from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel

from models.product import Product


# Define an enumeration for 'Side'
class Side(str, Enum):
    front = "front"
    back = "rear"


# Define an enumeration for 'Area'
class Area(str, Enum):
    MAIN_INVENTORY = "Main Inventory"
    PURIFIER = "Purifier"
    ENGINE_CONTROL = "Engine Control Room"


class Box(Document):
    deck: int
    area: Area
    zone: int
    level: int
    side: Side
    machine_name: str
    products: Optional[List[Link[Product]]]


class CreateBox(BaseModel):
    deck: int
    area: Area
    zone: int
    level: int
    side: Side
    machine_name: str
