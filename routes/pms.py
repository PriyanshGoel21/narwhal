from datetime import date, timedelta, datetime
from enum import Enum
from typing import List

from fastapi import APIRouter, Query, HTTPException

from models.jobs import Job, Status, Type, CompletedJob, CompletionStatus

router = APIRouter()


class Timeline(str, Enum):
    today = "today"
    week = "week"
    month = "month"


@router.get("/get_jobs")
async def jobs(
    status: Status = Query(None, description="Filter based on status"),
    due_within: Timeline = Query(None, description="Filter based on when it's due"),
) -> List[Job]:
    find = Job.find(fetch_links=True)
    if status:
        find = find.find(Job.status == status, fetch_links=True)
    if due_within:
        start = date.today()
        print(start)
        if due_within == "today":
            end = start + timedelta(days=1)
        elif due_within == "week":
            end = start + timedelta(days=7)
        else:
            end = start + timedelta(days=30)

        find = find.find(
            Job.due_date >= datetime(month=start.month, day=start.day, year=start.year),
            Job.due_date < datetime(month=end.month, day=end.day, year=end.year),
            fetch_links=True,
        )
    return await find.to_list()


@router.get("/jobs/status")
async def get_jobs(status: Status = Query(None, description="Get Jobs")) -> List[Job]:
    find = Job.find()
    if status:
        find = find.find(Job.status == status)

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
async def get_jobs_due(
    type: Type = Query(None, title="Time Range", description="Time Range")
):
    return await Job.find(Job.type == type).to_list()


@router.put("/jobs/{pms_code}/change_status")
async def change_status(
    pms_code: str,
    status: Status = Query(None, title="Status", description="Change Status"),
):
    job = await Job.find_one(Job.pms_code == pms_code, fetch_links=True)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    time_period = {Type.daily: 1, Type.weekly: 7, Type.monthly: 30}

    if status == Status.in_progress:
        today = date.today()
        job_due_date = datetime.fromisoformat(job.due_date.isoformat()).date()
        job.due_date = job_due_date + timedelta(days=time_period.get(job.type))
    elif status == Status.completed:
        today = date.today()

        job_due_date = datetime.fromisoformat(job.due_date.isoformat()).date()
        delta = job_due_date - today
        completion_status = (
            CompletionStatus.on_time if delta.days >= 0 else CompletionStatus.late
        )

        completed_job = CompletedJob(
            pms_code=job.pms_code,
            pms_desc=job.pms_desc,
            due_date=job_due_date,
            products=job.products,
            type=job.type,
            completion_status=completion_status,
        )
        await completed_job.save()

        job.status = Status.planning

    return await job.save()


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
