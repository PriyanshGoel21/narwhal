# import asyncio
# import csv
#
# from beanie import init_beanie, WriteRules
# from motor.motor_asyncio import AsyncIOMotorClient
#
# from models.jobs import Job
# from models.product import Product
#
#
# async def main():
#     # Beanie uses Motor async client under the hood
#     client = AsyncIOMotorClient(os.environ.get("DATABASE_URL"))
#
#     await init_beanie(database=client.narwhal, document_models=[Product, Job])
#     products = {}
#     jobs = {}
#     with open("products.csv", mode="r", encoding="utf8") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         line_count = 0
#         for row in csv_reader:
#             products[row["MATERIAL"]] = Product(
#                 material_code=row["MATERIAL"],
#                 material_desc=row["MATERIAL_DESC"],
#                 part_no=row["PART_NO"],
#                 rob=row["ROB"],
#                 scanned_quantity=0,
#                 work=row["WORK"],
#                 reconditioned=row["Recondition"],
#             )
#     with open("ok.csv", mode="r", encoding="utf8") as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             if jobs.get(row["pms_code"]):
#                 if row["part_code"] == "":
#                     continue
#                 jobs[row["pms_code"]].products.append(products[row["part_code"]])
#             else:
#                 jobs[row["pms_code"]] = Job(
#                     pms_code=row["pms_code"], pms_desc=row["pms_desc"], products=[]
#                 )
#                 if row["part_code"]:
#                     jobs[row["pms_code"]].products.append(products[row["part_code"]])
#     for job in jobs.values():
#         await job.insert(link_rule=WriteRules.WRITE)
#         print(job)
#     # print(products)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
