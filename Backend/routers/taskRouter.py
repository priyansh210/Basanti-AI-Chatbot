from fastapi import APIRouter, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from db_connection import db
from controllers.tasks_controller import TaskController
task_router = APIRouter()

@task_router.get("/", status_code=200)
async def get_tasks():
    return await TaskController.get_all_tasks()

@task_router.get("/{task_id}", status_code=200)
async def get_task(task_id: str):
    return await TaskController.get_task(task_id)

@task_router.post("/", status_code=201)
async def add_task(req: Request):
    req = await req.json()
    return await TaskController.add_task(req)

@task_router.delete("/{task_id}",status_code=204)
async def delete_task(task_id: str):
    return await TaskController.delete_task(task_id)
