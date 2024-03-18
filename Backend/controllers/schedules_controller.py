from bson.json_util import loads, dumps
from bson.objectid import ObjectId
import json

from db_connection import db

class ScheduleController:
    async def get_all_schedules():
        try:
            query = db.schedules.find({})
            return {"status": "successs",
                    "data": json.loads(dumps(query))}            
        except Exception as e:
            print(e)

    async def get_schedule(schedule_id: str):
        try:
            
            idObject = ObjectId(schedule_id)
            query = db.schedules.find({"_id": idObject})
            return {"status": "success",
                     "data": json.loads(dumps(query))
                    }
        except Exception as e:
            print(e)
    
    async def add_schedule(req):
        try:
            query = db.schedules.insert_one(req)
            id = str(query.inserted_id)
            return {"status": "successs",
                    "id": id
                    }
        except Exception as e:
            print(e)
    
    async def delete_schedule(schedule_id: str):
        try:
            
            idObject = ObjectId(schedule_id)
            query = db.schedules.delete_one({"_id": idObject})
            return {"status": "success"
                    }
        except Exception as e:
            print(e)

    


        
