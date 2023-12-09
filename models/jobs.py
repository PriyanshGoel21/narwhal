import uuid
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from beanie import Document
from typing import List
from zoneinfo import ZoneInfo


class Status(str, Enum):
    in_progress = "in_progress"
    completed = "completed"


class FilteringType(str, Enum):
    time_due = "time_due"
    time_created = "time_created"
    mach = "mach"
    pms_desc = "pms_desc"


class ProductRef(BaseModel):
    material_code: str
    req_quantity: int


class ListProductRef(BaseModel):
    products: List[ProductRef]


class Job(Document):
    job_id: uuid.UUID = uuid.uuid4()
    mach: str
    pms_desc: str
    created: float = datetime.timestamp(datetime.now())
    due: float
    status: Status = Status.in_progress
    spare_parts: ListProductRef


class CreateJob(BaseModel):
    mach: str
    pms_desc: str
    due: float
    spare_parts: ListProductRef


class AllJobs(BaseModel):
    jobs: List[Job]


class ChangeStatus(BaseModel):
    job_id: uuid.UUID
