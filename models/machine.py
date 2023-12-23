from typing import List

from beanie import Document, Link

from models.box import Box
from models.jobs import Job


class Machine(Document):
    machine_desc: str
    maker_desc: str
    jobs: List[Link[Job]]
    boxes: List[Link[Box]]
