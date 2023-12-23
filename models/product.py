from beanie import Document


class Product(Document):
    material_code: str
    material_desc: str
    part_no: str
    rob: int
    scanned_quantity: int
    work: int
    reconditioned: int
