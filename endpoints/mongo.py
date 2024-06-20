"""
usage
client: MongoDB
requirements: beanie, motor, pydantic
"""

from typing import List

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


class MongoClient:
    def __init__(self):
        self.uri = ""
        self.db = ""

    def init_config(self, config: dict):
        self.uri = config["uri"]
        self.database = config["database"]
        self.max_pool_size = config["max_pool_size"]
        self.min_pool_size = config["min_pool_size"]

    def new_client(self):
        return AsyncIOMotorClient(
            host=self.uri,
            maxPoolSize=self.max_pool_size,
            minPoolSize=self.min_pool_size,
        )

    async def connect(self, models: List[Document]):
        self.client = self.new_client()
        await init_beanie(self.client[self.database], document_models=models)

    async def disconnect(self):
        self.client.close()
