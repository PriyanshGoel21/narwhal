from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document, Link
from pydantic import Field

from models.product import Product


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
    due_date: datetime
    status: Status
    products: Optional[List[Link[Product]]]
    type: Type


class CompletedJob(Document):
    pms_code: str
    pms_desc: str
    due_date: datetime
    completed_date: datetime = Field(default_factory=datetime.now)
    products: Optional[List[Link[Product]]]
    type: Type
    completion_status: CompletionStatus
