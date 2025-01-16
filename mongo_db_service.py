from datetime import datetime
from typing import List
import uuid
import socket
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


class MongoDBService:
    def __init__(self, connection_uri: str, db_name: str, collection_name: str):
        """
        Initialize MongoDB connection and get collection reference.

        Args:
            connection_uri (str): MongoDB connection string
            db_name (str): Name of the database
            collection_name (str): Name of the collection
        """
        self.client: MongoClient = MongoClient(connection_uri)
        self.db: Database = self.client[db_name]
        self.collection: Collection = self.db[collection_name]

    def store_trending_topics(self, topics: List[str]) -> dict:
        """
        Store trending topics in MongoDB with required fields.

        Args:
            topics (List[str]): List of trending topics

        Returns:
            dict: Inserted document
        """
        # Ensure the topics list has exactly 5 items, filling missing ones with empty strings
        topics = (topics + [""] * 5)[:5]

        # Create document with required fields
        document = {
            "unique_id": str(uuid.uuid4()),
            "trend1": topics[0],
            "trend2": topics[1],
            "trend3": topics[2],
            "trend4": topics[3],
            "trend5": topics[4],
            "timestamp": datetime.now(),
            "ip_address": socket.gethostbyname(socket.gethostname())
        }

        # Insert document and return it
        self.collection.insert_one(document)
        return document

    def get_latest_trends(self, limit: int = 10) -> List[dict]:
        """
        Retrieve latest trending topics entries.

        Args:
            limit (int): Number of entries to retrieve

        Returns:
            List[dict]: List of trending topics documents
        """
        return list(
            self.collection
            .find({}, {'_id': 0})
            .sort('timestamp', -1)
            .limit(limit)
        )

    def close(self):
        """Close MongoDB connection."""
        self.client.close()