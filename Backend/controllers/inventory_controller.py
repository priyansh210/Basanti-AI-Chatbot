from bson.json_util import loads, dumps
from bson.objectid import ObjectId
import json
from db_connection import db
import fastapi


class InventoryController:
    async def get_all_inventory_items():
        try:
            query = db.inventory.find({})
            res = json.loads(dumps(query))
            # print(query)
            return {"status": "successs",
                    "data": res}
            
        except Exception as e:
            print(e)

    async def get_inventory_item(inventory_item_id: str):
        try:
            idObject = ObjectId(inventory_item_id)
            query = db.inventory.find({"_id": idObject})
            res = json.loads(dumps(query))
            if(len(res)):
                return fastapi.responses.JSONResponse(status_code=201, content={"status":"success", "data":res})
            else:
                return fastapi.responses.JSONResponse(status_code=404, content={"status":"fail"})
        except Exception as e:
            print(e)
    
    async def add_inventory_item(req):
        try:
            query = db.inventory.insert_one(req)
            id = str(query.inserted_id)
            # print("reached")
            return {"status": "successs",
                    "id": id
                    }
        except Exception as e:
            print(e)
    
    async def delete_inventory_item(inventory_item_id: str):
        try:
            
            idObject = ObjectId(inventory_item_id)
            query = db.inventory.delete_one({"_id": idObject})
            return {"status": "success"
                    }
        except Exception as e:
            print(e)

    


        
