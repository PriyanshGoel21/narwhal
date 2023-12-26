import datetime
from beanie import Link
from fastapi import APIRouter, Query, HTTPException
from typing import List
from models.jobs import Job, Status
from models.product import Product

router = APIRouter()


@router.get("/jobs/status")
async def get_jobs(status: Status = Query(None, title="Status", description="Get Jobs")) -> List[Job]:
    if status:
        jobs = await Job.find(Job.status == status).to_list()
    else:
        jobs = await Job.find_all().to_list()
    return jobs


@router.get("/jobs/all")
async def get_all_jobs() -> List[Job]:
    return await Job.find_all().to_list()


@router.get("/jobs/{pms_code}")
async def get_products_from_job(pms_code: str):
    try:
        job = await Job.find_one(Job.pms_code == pms_code, fetch_links=True)
        return job.products
    except:
        raise HTTPException(status_code=404, detail="Job not found")


@router.put("/jobs/{pms_code}/change_status")
async def change_status(pms_code: str, status: Status = Query(None, title="Status", description="Change Status")):
    try:
        job = await Job.find_one(Job.pms_code == pms_code, fetch_links=True)

        if job.status != status:
            job.status = status
            if status == status.in_progress:
                job.due_date = datetime.date.today().isoformat()  # placeholder until we find out how due date is
                # being assigned

        return await job.save()
    except:
        raise HTTPException(status_code=404, detail="Job not found")

