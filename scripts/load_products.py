import asyncio
import csv
import random

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.box import Box
from models.jobs import Job
from models.product import Product


async def main():
    # Beanie uses Motor async client under the hood
    client = AsyncIOMotorClient("mongodb://narwhal:narwhal123@159.89.204.17:27017")

    await init_beanie(database=client.narwhal, document_models=[Product, Job, Box])
    products = {}
    jobs = {}
    machine = {}
    with open("products.csv", mode="r", encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            # products[row["MATERIAL"]] = Product(
            #     material_code=row["MATERIAL"],
            #     material_desc=row["MATERIAL_DESC"],
            #     part_no=row["PART_NO"],
            #     rob=row["ROB"],
            #     scanned_quantity=0,
            #     work=row["WORK"],
            #     reconditioned=row["Recondition"],
            # )
            if machine.get(row["MACH_DESC"]) is None:
                machine[row["MACH_DESC"]] = list()
            product = await Product.find_one(Product.material_code == row["MATERIAL"])
            # machine[row["MACH_DESC"]].append(
            #     Product(
            #         material_code=row["MATERIAL"],
            #         material_desc=row["MATERIAL_DESC"],
            #         part_no=row["PART_NO"],
            #         rob=row["ROB"],
            #         scanned_quantity=0,
            #         work=row["WORK"],
            #         reconditioned=row["Recondition"],
            #     )
            # )
            line_count += 1
            print(line_count)
            machine[row["MACH_DESC"]].append(product)

    # with open("ok.csv", mode="r", encoding="utf8") as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     for row in csv_reader:
    #         if jobs.get(row["pms_code"]):
    #             if row["part_code"] == "":
    #                 continue
    #             jobs[row["pms_code"]].products.append(products[row["part_code"]])
    #         else:
    #             jobs[row["pms_code"]] = Job(
    #                 pms_code=row["pms_code"], pms_desc=row["pms_desc"], products=[]
    #             )
    #             if row["part_code"]:
    #                 jobs[row["pms_code"]].products.append(products[row["part_code"]])
    # for job in jobs.values():
    #     await job.insert(link_rule=WriteRules.WRITE)
    #     print(job)
    print(machine)
    decks = [deck for deck in range(1, 4)]
    areas = ["A", "B", "C"]
    zones = [zone for zone in range(1, 6)]
    levels = [level for level in range(1, 4)]
    sides = ["front", "rear"]
    types = ["metal", "cardboard"]
    for deck in decks:
        for area in areas:
            for zone in zones:
                for level in levels:
                    for box in range(1, random.randint(5, 14)):
                        for side in sides:
                            machinee = random.choice(list(machine.keys()))
                            types = ["metal", "cardboard"]
                            box = Box(
                                deck=deck,
                                area=area,
                                zone=zone,
                                level=level,
                                side=side,
                                type=random.choice(types),
                                products=machine[machinee],
                                machine_name=machinee,
                            )
                            await box.insert()
    # print(products)


if __name__ == "__main__":
    asyncio.run(main())
