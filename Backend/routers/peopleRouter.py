from fastapi import APIRouter, HTTPException, Request
from controllers.people_controller import PeopleController

people_router = APIRouter()

# @people_router.get("/", status_code=200)
# async def get_messages():
#     return await MessageController.get_all_messages()

# @message_router.get("/{message_id}", status_code=200)
# async def get_message(message_id: str):
#     return await MessageController.get_message(message_id)

@people_router.post("/", status_code=201)
async def add_person(req: Request):
    req = await req.json()
    return await PeopleController.add_person(req)

@people_router.get("/", status_code=200)
async def get_people():
    return await PeopleController.get_people()

@people_router.get("/{person_name}")
async def get_person_by_name(person_name):
    print(person_name)
    return await PeopleController.get_person_by_name( person_name  )

# @message_router.delete("/{message_id}",status_code=204)
# async def delete_message(message_id: str):
#     return await MessageController.delete_message(message_id)
