from enum import Enum

from beanie import Document


# {"SERIALNO": "45383537", "PRODUCT": "9008152", "EPC": "301A94B9E262858002B47F71", "COMPANY": "BWS"}
class Side(str, Enum):
    front = "front"
    back = "rear"


class Box(Document):
    zone: int
    level: int
    box: int
    side: Side
    serial_no: int
    product: int
    epc: str
    company: str
