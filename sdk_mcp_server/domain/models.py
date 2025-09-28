"""Domain models for article data."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Article:
    """Article domain model."""

    id: str
    thumbnail_image_url: str  # Supabase public URL instead of local path
    title: str
    subtitle: str
    video_file_url: Optional[str] = None  # Supabase public URL instead of local path
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Convert article to dictionary for MongoDB storage."""
        return {
            "id": self.id,
            "thumbnail_image_url": self.thumbnail_image_url,
            "video_file_url": self.video_file_url,
            "title": self.title,
            "subtitle": self.subtitle,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Article":
        """Create article from dictionary."""
        return cls(
            id=data["id"],
            thumbnail_image_url=data["thumbnail_image_url"],
            title=data["title"],
            subtitle=data["subtitle"],
            video_file_url=data.get("video_file_url"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


@dataclass
class ArticleCreationInput:
    """Input model for creating articles."""

    id: str
    thumbnail_image_url: str  # Supabase public URL
    title: str
    subtitle: str
    video_file_url: Optional[str] = None  # Supabase public URL


@dataclass
class ArticleCreationRequest:
    """Request model for creating articles with local image path."""
    id: str
    thumbnail_image_path: str  # Local path that will be uploaded to Supabase
    title: str
    subtitle: str
    video_file_path: Optional[str] = None


@dataclass
class ArticleUpdateInput:
    """Input model for updating articles."""
    id: str
    thumbnail_image_path: Optional[str] = None  # Local path that will be uploaded to Supabase
    title: Optional[str] = None
    subtitle: Optional[str] = None
    video_file_path: Optional[str] = None


## json schema
article_creation_request_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "thumbnail_image_path": {"type": "string"},
        "video_file_path": {"type": "string", "nullable": True},
        "title": {"type": "string"},
        "subtitle": {"type": "string"}
    },
    "required": ["id", "thumbnail_image_path", "title", "subtitle"]
}

article_update_input_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "thumbnail_image_path": {"type": "string"},
        "title": {"type": "string"},
        "subtitle": {"type": "string"},
        "video_file_path": {"type": "string", "nullable": True}
    },
    "required": ["id"]
}