from typing import List, Optional
from beanie import Document, Link
from models.product import Product
from enum import Enum


class Status(str, Enum):
    in_progress = "in_progress"
    completed = "completed"
    planning = "planning"


class Job(Document):
    pms_code: str
    pms_desc: str
    due_date: str
    status: Status
    products: Optional[List[Link[Product]]]

