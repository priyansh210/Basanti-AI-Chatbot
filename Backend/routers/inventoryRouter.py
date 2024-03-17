from fastapi import APIRouter, HTTPException, Request
from controllers.inventory_controller import InventoryController
from motor.motor_asyncio import AsyncIOMotorClient
from db_connection import db

inventory_router = APIRouter()

@inventory_router.get("/", status_code=200)
async def get_inventorys():
    return await InventoryController.get_all_inventory_items()

@inventory_router.get("/{inventory_id}", status_code=200)
async def get_inventory(inventory_id: str):
    return await InventoryController.get_inventory_item(inventory_id)

@inventory_router.post("/", status_code=201)
async def add_inventory(req: Request):
    req = await req.json()
    return await InventoryController.add_inventory_item(req)

@inventory_router.delete("/{inventory_id}",status_code=204)
async def delete_inventory(inventory_id: str):
    return await InventoryController.delete_inventory_item(inventory_id)
