"""MongoDB Atlas client configuration."""

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database


class MongoDBClient:
    """MongoDB Atlas client wrapper."""

    def __init__(self, connection_string: Optional[str] = None, database_name: Optional[str] = None):
        """Initialize MongoDB client."""
        self.connection_string = connection_string or os.getenv("MONGODB_URL")  # Updated to match actual env var
        self.database_name = database_name or os.getenv("MONGODB_DATABASE", "aitimes")

        if not self.connection_string:
            raise ValueError("MongoDB connection string is required")

        self._client: Optional[MongoClient] = None
        self._database: Optional[Database] = None

    def connect(self) -> None:
        """Connect to MongoDB Atlas."""
        try:
            self._client = MongoClient(self.connection_string)
            self._database = self._client[self.database_name]
            # Test connection
            self._client.admin.command('ping')
            print(f"🍀 Successfully connected to MongoDB Atlas database: aitimes")
        except Exception as e:
            print(f"Failed to connect to MongoDB Atlas: {e}")
            raise

    def disconnect(self) -> None:
        """Disconnect from MongoDB Atlas."""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            print("Disconnected from MongoDB Atlas")

    @property
    def database(self) -> Database:
        """Get database instance."""
        if not self._database:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._database

    @property
    def client(self) -> MongoClient:
        """Get client instance."""
        if not self._client:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self._client

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()