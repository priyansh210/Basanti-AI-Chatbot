from fastapi import APIRouter, HTTPException, Request
from db_connection import db
from controllers.schedules_controller import ScheduleController
schedule_router = APIRouter()

@schedule_router.get("/", status_code=200)
async def get_schedules():
    return await ScheduleController.get_all_schedules()

@schedule_router.get("/{schedule_id}", status_code=200)
async def get_schedule(schedule_id: str):
    return await ScheduleController.get_schedule(schedule_id)

@schedule_router.post("/", status_code=201)
async def add_schedule(req: Request):
    req = await req.json()
    return await ScheduleController.add_schedule(req)

@schedule_router.delete("/{schedule_id}",status_code=204)
async def delete_schedule(schedule_id: str):
    return await ScheduleController.delete_schedule(schedule_id)
