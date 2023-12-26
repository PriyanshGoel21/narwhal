import asyncio
import csv
import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.product import Product2


async def main():
    client = AsyncIOMotorClient(os.environ.get("DATABASE_URL"))

    await init_beanie(database=client.test, document_models=[Product2])

    with open("products.csv", mode="r", encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(row["MATERIAL"])
            product = await Product2.find_one(Product2.material_code == row["MATERIAL"])
            if product is None:
                product = Product2(
                    machine=row["MACH_DESC"],
                    material_code=row["MATERIAL"],
                    material_desc=row["MATERIAL_DESC"],
                    part_no=row["PART_NO"],
                    rob=row["ROB"],
                    scanned_quantity=0,
                    work=row["WORK"],
                    reconditioned=row["Recondition"],
                )
                await product.insert()


if __name__ == "__main__":
    asyncio.run(main())
