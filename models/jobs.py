from typing import List, Optional
from beanie import Document, Link
from models.product import Product
from enum import Enum


class Status(str, Enum):
    in_progress = "in_progress"
    completed = "completed"
    planning = "planning"


class Type(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class CompletionStatus(str, Enum):
    on_time = "on_time"
    late = "late"


class Job(Document):
    pms_code: str
    pms_desc: str
    due_date: str
    completed_date: Optional[str]
    status: Status
    products: Optional[List[Link[Product]]]
    type: Type


class CompletedJob(Document):
    pms_code: str
    pms_desc: str
    due_date: str
    completed_date: Optional[str]
    products: Optional[List[Link[Product]]]
    type: Type
    completion_status: CompletionStatus
