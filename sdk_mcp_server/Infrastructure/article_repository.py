"""Article repository for MongoDB operations."""

from datetime import datetime
from typing import List, Optional

from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

from ..domain.models import Article, ArticleCreationInput, ArticleUpdateInput
from .mongodb_client import MongoDBClient


class ArticleRepository:
    """Repository for article operations in MongoDB."""

    def __init__(self, mongodb_client: MongoDBClient):
        """Initialize article repository."""
        self.mongodb_client = mongodb_client
        self.collection_name = "articles"

    @property
    def collection(self) -> Collection:
        """Get articles collection."""
        return self.mongodb_client.database[self.collection_name]

    async def create_article(self, article_input: ArticleCreationInput) -> Article:
        """Create a new article."""
        now = datetime.utcnow()
        article = Article(
            id=article_input.id,
            thumbnail_image_url=article_input.thumbnail_image_url,
            title=article_input.title,
            subtitle=article_input.subtitle,
            video_file_url=article_input.video_file_url,
            created_at=now,
            updated_at=now
        )

        try:
            result = self.collection.insert_one(article.to_dict())
            if not result.acknowledged:
                raise RuntimeError("Failed to insert article")
            return article
        except DuplicateKeyError:
            raise ValueError(f"Article with id '{article_input.id}' already exists")

    async def get_article_by_id(self, article_id: str) -> Optional[Article]:
        """Get article by ID."""
        document = self.collection.find_one({"id": article_id})
        if document:
            return Article.from_dict(document)
        return None

    async def update_article(self, article_id: str, update_input: ArticleUpdateInput) -> Optional[Article]:
        """Update an existing article."""
        update_data = {}
        if update_input.thumbnail_image_html_screenshot_path is not None:
            update_data["thumbnail_image_html_screenshot_path"] = update_input.thumbnail_image_html_screenshot_path
        if update_input.title is not None:
            update_data["title"] = update_input.title
        if update_input.subtitle is not None:
            update_data["subtitle"] = update_input.subtitle

        if not update_data:
            # No updates provided, return current article
            return await self.get_article_by_id(article_id)

        update_data["updated_at"] = datetime.utcnow()

        result = self.collection.update_one(
            {"id": article_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            return None

        return await self.get_article_by_id(article_id)

    async def delete_article(self, article_id: str) -> bool:
        """Delete an article by ID."""
        result = self.collection.delete_one({"id": article_id})
        return result.deleted_count > 0

    async def list_articles(self, limit: int = 100, offset: int = 0) -> List[Article]:
        """List articles with pagination."""
        cursor = self.collection.find().skip(offset).limit(limit).sort("created_at", -1)
        articles = []
        for document in cursor:
            articles.append(Article.from_dict(document))
        return articles

    async def count_articles(self) -> int:
        """Count total number of articles."""
        return self.collection.count_documents({})

    def create_indexes(self) -> None:
        """Create necessary indexes for the collection."""
        # Create unique index on id field
        self.collection.create_index("id", unique=True)
        # Create index on created_at for sorting
        self.collection.create_index("created_at")
        print(f"Created indexes for {self.collection_name} collection")