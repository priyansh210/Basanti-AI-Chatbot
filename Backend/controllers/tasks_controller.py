from bson.json_util import loads, dumps
from bson.objectid import ObjectId
import json

from db_connection import db

class TaskController:
    async def get_all_tasks():
        try:
            query = db.tasks.find({})
            return {"status": "successs",
                    "data": json.loads(dumps(query))}            
        except Exception as e:
            print(e)

    async def get_task(task_id: str):
        try:
            
            idObject = ObjectId(task_id)
            query = db.tasks.find({"_id": idObject})
            return {"status": "success",
                     "data": json.loads(dumps(query))
                    }
        except Exception as e:
            print(e)
    
    async def add_task(req):
        try:
            query = db.tasks.insert_one(req)
            id = str(query.inserted_id)
            return {"status": "successs",
                    "id": id
                    }
        except Exception as e:
            print(e)
    
    async def delete_task(task_id: str):
        try:
            
            idObject = ObjectId(task_id)
            query = db.tasks.delete_one({"_id": idObject})
            return {"status": "success"
                    }
        except Exception as e:
            print(e)

    


        
