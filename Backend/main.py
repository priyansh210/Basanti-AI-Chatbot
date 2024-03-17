from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
#all routers
from routers.messageRouter import message_router
from routers.taskRouter import task_router
from routers.scheduleRouter import schedule_router
from routers.updateRouter import update_router
from routers.peopleRouter import people_router
from routers.inventoryRouter import inventory_router
#pymongo - for db connection
from db_connection import db
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os

load_dotenv()
@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        mongo_uri = os.environ.get("MONGO_URI")
        db.connect_to_database(path=mongo_uri)
        print("connected to db in main.py!")

        yield
        db.close_database_connection()
        # client.close()
    except Exception as e:
        print(e)

app = FastAPI(lifespan= lifespan)
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
	
)


@app.get("/")
async def landing():
    return {"message": "success"}
#routing
app.include_router(message_router, prefix="/messages")
app.include_router(task_router, prefix="/tasks")
app.include_router(schedule_router, prefix="/schedules")
app.include_router(update_router, prefix="/update")
app.include_router(people_router, prefix="/people")
app.include_router(inventory_router, prefix="/inventory")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload="true")
