from schema.messageSchema import MessageSchema
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
import json

from db_connection import db
import fastapi
from models.validation_error import ValidationError

class PeopleController:
    async def get_people():
        try:
            query = db.people.find({})
            res = json.loads(dumps(query))
            if(len(res)):
                return fastapi.responses.JSONResponse(status_code=201, content={"status":"success", "data":res})
            else:
                return fastapi.responses.JSONResponse(status_code=404, content={"status":"fail"})
        except ValidationError as ve:
            return fastapi.Response(content=ve.error_msg, status_code=ve.status_code)
        except Exception as e:
            return fastapi.Response(content=str(e), status_code=500)
    
    async def add_person(req):
        try:
            query = db.people.insert_one(req)
            # res = json.loads(dumps(query))
            # print(res)
            id = str(query.inserted_id)
            if(id):
                return fastapi.responses.JSONResponse(status_code=201, content={"status":"success", "id":id})
            else:
                return fastapi.responses.JSONResponse(status_code=404, content={"status":"fail"})
                    
        except Exception as e:
            return fastapi.Response(content=str(e), status_code=500)

    async def get_person_by_name(name: str):
        try:
            query = db.people.find_one({"properties.name": {"$regex": f".*{name}.*", "$options": "i"}})
            res = json.loads(dumps(query))
            # print(res)
            if(res):
                return fastapi.responses.JSONResponse(status_code=201, content={"status":"success", "data":res})
            else:
                return fastapi.responses.JSONResponse(status_code=404, content={"status":"fail"})       
        except Exception as e:
            return fastapi.Response(content=str(e), status_code=500)
    
    # async def delete_message(message_id: str) -> MessageSchema:
    #     try:
            
    #         idObject = ObjectId(message_id)
    #         query = db.messages.delete_one({"_id": idObject})
    #         return {"status": "success"
    #                 }
    #     except Exception as e:
    #         print(e)

    


        
