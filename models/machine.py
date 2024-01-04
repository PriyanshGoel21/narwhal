from typing import List

from beanie import Document, Link

from models.jobs import Job


class Machine(Document):
    machine_desc: str
    maker_desc: str
    jobs: List[Link[Job]]
