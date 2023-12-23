from typing import List, Optional

from beanie import Document, Link

from models.product import Product


class Job(Document):
    pms_code: str
    pms_desc: str
    products: Optional[List[Link[Product]]]
