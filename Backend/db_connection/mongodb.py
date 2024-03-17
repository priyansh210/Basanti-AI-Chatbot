from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
load_dotenv()
async def get_mongo_db():
    print("hi")
    mongo_uri = os.environ.get("MONGO_URI")
    client = AsyncIOMotorClient(mongo_uri)
    try:
        await client.admin.command('ping')
        print("Connected to server")
        
    except Exception as e:
        print(e)
    return client.basanti_backend
    