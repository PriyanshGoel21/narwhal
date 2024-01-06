from typing import List, Optional
from beanie import Document, Link
from models.product import Product
from enum import Enum
import datetime
from pydantic import Field

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
    due_date: Optional[datetime.datetime]
    status: Status
    products: Optional[List[Link[Product]]]
    type: Type


class CompletedJob(Document):
    pms_code: str
    pms_desc: str
    due_date: datetime.date
    completed_date: datetime.date = Field(default_factory=datetime.date)
    products: Optional[List[Link[Product]]]
    type: Type
    completion_status: CompletionStatus
