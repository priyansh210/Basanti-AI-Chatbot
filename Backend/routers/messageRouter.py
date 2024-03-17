from fastapi import APIRouter, HTTPException, Request
from controllers.messages_controller import MessageController
from motor.motor_asyncio import AsyncIOMotorClient
from db_connection import db

message_router = APIRouter()

@message_router.get("/", status_code=200)
async def get_messages():
    return await MessageController.get_all_messages()

@message_router.get("/{message_id}", status_code=200)
async def get_message(message_id: str):
    return await MessageController.get_message(message_id)

@message_router.post("/", status_code=201)
async def add_message(req: Request):
    req = await req.json()
    return await MessageController.add_message(req)

@message_router.delete("/{message_id}",status_code=204)
async def delete_message(message_id: str):
    return await MessageController.delete_message(message_id)
