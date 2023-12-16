import uuid
from typing import List

from fastapi import APIRouter, Query, HTTPException

from legacy.models.jobs import Job, FilteringType, Status, CreateJob
from legacy.models.product import Product

router = APIRouter()  # Create an instance of an APIRouter


# 1. Creating a Job
@router.post("/create_job")
async def create_job(job: CreateJob) -> Job:
    spare_parts = list()
    for spare_part in job.spare_parts.products:
        product = await Product.find_one(Product.product_id == spare_part.material_code)
        if product:
            spare_parts.append(
                {
                    "material_code": spare_part.material_code,
                    "req_quantity": spare_part.req_quantity,
                }
            )
    new_job = Job(
        mach=job.mach,
        pms_desc=job.pms_desc,
        due=job.due,
        spare_parts={"products": spare_parts},
    )
    return await new_job.insert()


# 2. Listing and getting all Jobs
@router.get("/get_all_jobs")
async def get_all_jobs() -> List[Job]:
    return await Job.find_all().to_list()


# 3. Listing and getting a specified quantity of jobs. (filtering - time due/ time created/ any other)
@router.get("/get_specific_jobs")
async def get_specific_jobs(
    filter: FilteringType = Query(..., description="Select Type of Filter"),
    quantity: int = Query(..., description="Enter quantity of Jobs required"),
) -> List[Job]:
    if filter == FilteringType.time_due:
        jobs = await Job.find().limit(quantity).to_list()
    elif filter == FilteringType.time_created:
        jobs = await Job.find().limit(quantity).to_list()
    else:
        jobs = await Job.find({filter: {"$exists": True}}).limit(quantity).to_list()
    return jobs


# 4. Changing the status of a particular job
@router.put("/change_status")
async def change_status(job_id: str, status: Status):
    job = await Job.find_one(Job.job_id == uuid.UUID(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.status = status
    await job.save()


# 5. Getting the quantity of products required for a particular job available in the inventory
@router.get("/get_job_products/{job_id}")
async def get_job_products(job_id: str):
    job = await Job.find_one(Job.job_id == uuid.UUID(job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for product in job.spare_parts.products:
        product.existing_quantity = await get_quantity_of_material(
            product.material_desc
        )
    return job.spare_parts


# 6. Getting the quantity of products required for a particular job available in the inventory
