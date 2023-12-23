import asyncio
import csv
import os

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.product import Product


async def main():
    # Beanie uses Motor async client under the hood
    client = AsyncIOMotorClient(os.environ.get("DATABASE_URL"))

    await init_beanie(database=client.narwhal, document_models=[Product])

    with open("products.csv", mode="r", encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            print(row["MATERIAL"])
            product = await Product.find_one(Product.material_code == row["MATERIAL"])
            if product is None:
                product = Product(
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
