from datetime import date, timedelta
from beanie import Link
from fastapi import APIRouter, Query, HTTPException
from typing import List
from models.jobs import Job, Status, Type, CompletedJob, CompletionStatus
from models.product import Product

router = APIRouter()


@router.get("/jobs/status")
async def get_jobs(status: Status = Query(None, title="Status", description="Get Jobs")) -> List[Job]:
    if status:
        jobs = await Job.find(Job.status == status).to_list()
    else:
        jobs = await Job.find_all().to_list()
    return jobs


@router.get("/jobs/filtered/all")
async def get_all_jobs() -> List[Job]:
    return await Job.find_all().to_list()


@router.get("/jobs/{pms_code}")
async def get_products_from_job(pms_code: str):
    try:
        job = await Job.find_one(Job.pms_code == pms_code, fetch_links=True)
        return job.products
    except:
        raise HTTPException(status_code=404, detail="Job not found")


@router.get("jobs/filtered/due")
async def get_jobs_due():
    pass


@router.put("/jobs/{pms_code}/change_status")
async def change_status(pms_code: str, status: Status = Query(None, title="Status", description="Change Status")):
    try:
        job = await Job.find_one(Job.pms_code == pms_code, fetch_links=True)

        time_period = {Type.daily: 1, Type.weekly: 7, Type.monthly: 30}

        if status == Status.in_progress:
            today = date.today()
            job.due_date = today + timedelta(days=time_period.get(job.type))
        elif status == Status.completed:
            today = date.today()

            delta = job.due_date - today
            completion_status = (CompletionStatus.on_time if delta.days >= 0 else CompletionStatus.late)

            completed_job = CompletedJob(
                pms_code=job.pms_code,
                pms_desc=job.pms_desc,
                due_date=job.due_date,
                products=job.products,
                type=job.type,
                completion_status=completion_status
            )
            await completed_job.save()

            job.status = Status.planning
        return await job.save()


    except:
        raise HTTPException(status_code=404, detail="Job not found")


@router.get("jobs/{pms_code}/drawings")
async def get_drawings(pms_code: str):
    try:
        return "Feature work in progress"

    except:
        raise HTTPException(status_code=404, detail="Drawing not found")


@router.get("jobs/{pms_code}/instructions")
async def get_drawings(pms_code: str):
    try:
        return "Feature work in progress"

    except:
        raise HTTPException(status_code=404, detail="Instructions not found")
