import asyncio
import datetime

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.jobs import Job


async def main():
    client = AsyncIOMotorClient("mongodb://narwhal:narwhal123@159.89.204.17:27017")
    await init_beanie(database=client.narwhal, document_models=[Job])

    jobs = await Job.find().to_list()
    print(jobs)
    for day, job in enumerate(jobs):
        job.due_date = datetime.date.today() + datetime.timedelta(days=day // 5)
        print(day, job)
        await job.save()
    # with open("products.csv", mode="r", encoding="utf8") as csv_file:
    #     print("ok")
    #     csv_reader = csv.DictReader(csv_file)
    #     for row in csv_reader:
    #         product = await Product.find_one(Product.material_code == row["MATERIAL"])
    #         if product is None:
    #             print(row["MATERIAL"])
    #             product = Product(
    #                 machine=row["MACH_DESC"],
    #                 material_code=row["MATERIAL"],
    #                 material_desc=row["MATERIAL_DESC"],
    #                 part_no=row["PART_NO"],
    #                 rob=row["ROB"],
    #                 scanned_quantity=0,
    #                 work=row["WORK"],
    #                 reconditioned=row["Recondition"],
    #             )
    #             await product.insert()


if __name__ == "__main__":
    asyncio.run(main())
