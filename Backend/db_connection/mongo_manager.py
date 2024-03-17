import logging
from pymongo import MongoClient, collection
from pymongo.database import Database

class MongoManager:
    client: MongoClient = None
    db: Database = None
    messages: collection = None
    tasks: collection = None
    schedules: collection = None
    people: collection = None
    inventory: collection = None

    def connect_to_database(self, path: str):
        logging.info("Connecting to MongoDB.")
        self.client = MongoClient(path)
        self.db = self.client.basanti_backend
        self.messages = self.db["messages"]
        self.tasks = self.db["tasks"]
        self.schedules = self.db["schedules"]
        self.people = self.db["people"]
        self.inventory = self.db["inventory"]
        logging.info("Connected to MongoDB.")

    def close_database_connection(self):
        logging.info("Closing connection with MongoDB.")
        self.client.close()
        logging.info("Closed connection with MongoDB.")