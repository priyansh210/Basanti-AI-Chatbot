from bson.json_util import loads, dumps
from bson.objectid import ObjectId
from db_connection import db


class UpdateController:
    async def update_any(req: dict):
        try:
            mp = {"messages": db.messages, "tasks": db.tasks, "schedules": db.schedules,"inventory": db.inventory}
            print(req)
            collection = mp[req["collection"]]
            query = collection.update_one({"_id":ObjectId(req["id"])}, {"$set":req["properties"] })

            return {"status": "successs"}
            
        except Exception as e:
            print(e)

    
# {
#     "collection": "", e.g messages tasks schedules people
#     "id": "",
#     "properties": {...}
# }

        
