from enum import Enum
from beanie import Document
from pydantic import BaseModel


# from typing import Optional
# from pydantic import BaseModel


# {"SERIALNO": "45383537", "PRODUCT": "9008152", "EPC": "301A94B9E262858002B47F71", "COMPANY": "BWS"}
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


class FetchBoxesFromZone(BaseModel):
    company: str
    product_id: str
