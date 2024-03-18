from fastapi import APIRouter, Request
from controllers.updates_controller import UpdateController
update_router = APIRouter()

@update_router.patch("/", status_code=201)
async def updateDocument(req: Request):
    req = await req.json()
    return await UpdateController.update_any(req)