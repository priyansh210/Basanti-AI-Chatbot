from schema.messageSchema import MessageSchema
from bson.json_util import loads, dumps
from bson.objectid import ObjectId
import json
from fastapi import HTTPException
from db_connection import db
import fastapi

from typing import List


class MessageController:
    # async def get_all_messages(db=Depends(get_mongo_db)) -> List[MessageSchema]:
    #     try:
    #         # messages_collection = db.get_collection("messages")
    #         # print(messages_collection)
    #         # result = await messages_collection.find_one()

    #         return {"message": "successs",
    #                 "data": ""}
    #     except Exception as e:
    #         print(e)
    async def get_all_messages() -> List[MessageSchema]:
        try:
            #print(db)
            # mydb = db.client["basanti_backend"]
            # collection = mydb["messages"]
            query = db.messages.find({})
            res = json.loads(dumps(query))
            # print(query)
            return {"status": "successs",
                    "data": res}
            
        except Exception as e:
            print(e)

    async def get_message(message_id: str) -> MessageSchema:
        try:
            idObject = ObjectId(message_id)
            query = db.messages.find({"_id": idObject})
            res = json.loads(dumps(query))
            if(len(res)):
                return fastapi.responses.JSONResponse(status_code=201, content={"status":"success", "data":res})
            else:
                return fastapi.responses.JSONResponse(status_code=404, content={"status":"fail"})
        except Exception as e:
            print(e)
    
    async def add_message(req):
        try:
            query = db.messages.insert_one(req)
            id = str(query.inserted_id)
            # print("reached")
            return {"status": "successs",
                    "id": id
                    }
        except Exception as e:
            print(e)
    
    async def delete_message(message_id: str) -> MessageSchema:
        try:
            
            idObject = ObjectId(message_id)
            query = db.messages.delete_one({"_id": idObject})
            return {"status": "success"
                    }
        except Exception as e:
            print(e)

    


        
