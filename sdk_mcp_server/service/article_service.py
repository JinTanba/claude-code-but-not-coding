"""Article service that handles image upload and article creation."""

from ..domain.models import Article, ArticleCreationInput, ArticleCreationRequest
from ..Infrastructure.article_repository import ArticleRepository
from .image_upload_service import FileUploadService


class ArticleService:
    """Service for handling article creation with image and video upload."""

    def __init__(self, article_repository: ArticleRepository, file_service: FileUploadService):
        """Initialize article service."""
        self.article_repository = article_repository
        self.file_service = file_service

    async def create_article_with_upload(self, request: ArticleCreationRequest) -> Article:
        """
        Create an article by uploading files to Supabase first.

        Args:
            request: Article creation request with local file paths

        Returns:
            Created article with Supabase URLs

        Raises:
            FileNotFoundError: If required files don't exist
            ValueError: If validation fails
            RuntimeError: If upload or creation fails
        """
        # Validate input
        if not request.id or not request.id.strip():
            raise ValueError("Article ID is required")
        if not request.title or not request.title.strip():
            raise ValueError("Article title is required")
        if not request.subtitle or not request.subtitle.strip():
            raise ValueError("Article subtitle is required")

        # Validate thumbnail image
        if not self.file_service.validate_image_path(request.thumbnail_image_path):
            raise ValueError(f"Invalid image path or format: {request.thumbnail_image_path}")

        if not self.file_service.validate_image_size(request.thumbnail_image_path):
            raise ValueError("Image file is too large (max 10MB)")

        # Upload thumbnail image to Supabase
        try:
            thumbnail_url = self.file_service.upload_thumbnail_image(
                request.thumbnail_image_path,
                request.id
            )
        except Exception as e:
            raise RuntimeError(f"Failed to upload thumbnail image: {str(e)}")

        # Upload video if provided
        video_url = None
        if request.video_file_path:
            # Validate video
            if not self.file_service.validate_video_path(request.video_file_path):
                # Clean up thumbnail if video validation fails
                self.file_service.delete_thumbnail_image(thumbnail_url)
                raise ValueError(f"Invalid video path or format: {request.video_file_path}")

            if not self.file_service.validate_video_size(request.video_file_path):
                # Clean up thumbnail if video validation fails
                self.file_service.delete_thumbnail_image(thumbnail_url)
                raise ValueError("Video file is too large (max 100MB)")

            try:
                video_url = self.file_service.upload_video_file(
                    request.video_file_path,
                    request.id
                )
            except Exception as e:
                # Clean up thumbnail if video upload fails
                self.file_service.delete_thumbnail_image(thumbnail_url)
                raise RuntimeError(f"Failed to upload video file: {str(e)}")

        # Create article with uploaded URLs
        article_input = ArticleCreationInput(
            id=request.id,
            thumbnail_image_url=thumbnail_url,
            video_file_url=video_url,
            title=request.title,
            subtitle=request.subtitle
        )

        try:
            return await self.article_repository.create_article(article_input)
        except Exception as e:
            # Try to clean up uploaded files if article creation fails
            self.file_service.delete_thumbnail_image(thumbnail_url)
            if video_url:
                self.file_service.delete_video_file(video_url)
            raise RuntimeError(f"Failed to create article: {str(e)}")

    async def get_article(self, article_id: str) -> Article:
        """Get an article by ID."""
        if not article_id or not article_id.strip():
            raise ValueError("Article ID is required")

        article = await self.article_repository.get_article_by_id(article_id)
        if not article:
            raise ValueError(f"Article not found: {article_id}")

        return article

    async def delete_article(self, article_id: str) -> bool:
        """Delete an article and its thumbnail image."""
        # Get article first to get image URL
        try:
            article = await self.get_article(article_id)
        except ValueError:
            return False  # Article doesn't exist

        # Delete from database
        deleted = await self.article_repository.delete_article(article_id)

        if deleted:
            # Try to delete files from Supabase (best effort)
            self.file_service.delete_thumbnail_image(article.thumbnail_image_url)
            if article.video_file_url:
                self.file_service.delete_video_file(article.video_file_url)

        return deleted

    async def list_articles(self, limit: int = 100, offset: int = 0) -> list[Article]:
        """List articles with pagination."""
        if limit <= 0 or limit > 1000:
            raise ValueError("Limit must be between 1 and 1000")
        if offset < 0:
            raise ValueError("Offset must be non-negative")

        return await self.article_repository.list_articles(limit, offset)

    async def update_article(self, article_id: str, update_data: dict) -> Article:
        """Update an article with new data."""
        if not article_id or not article_id.strip():
            raise ValueError("Article ID is required")

        # Get existing article first
        existing_article = await self.get_article(article_id)

        # Handle file uploads if new paths are provided
        thumbnail_url = existing_article.thumbnail_image_url
        video_url = existing_article.video_file_url

        # Upload new thumbnail if provided
        if update_data.get("thumbnail_image_path"):
            if not self.file_service.validate_image_path(update_data["thumbnail_image_path"]):
                raise ValueError(f"Invalid image path or format: {update_data['thumbnail_image_path']}")

            if not self.file_service.validate_image_size(update_data["thumbnail_image_path"]):
                raise ValueError("Image file is too large (max 10MB)")

            try:
                new_thumbnail_url = self.file_service.upload_thumbnail_image(
                    update_data["thumbnail_image_path"],
                    article_id
                )
                # Delete old thumbnail
                self.file_service.delete_thumbnail_image(thumbnail_url)
                thumbnail_url = new_thumbnail_url
            except Exception as e:
                raise RuntimeError(f"Failed to upload new thumbnail: {str(e)}")

        # Upload new video if provided
        if update_data.get("video_file_path"):
            if not self.file_service.validate_video_path(update_data["video_file_path"]):
                raise ValueError(f"Invalid video path or format: {update_data['video_file_path']}")

            if not self.file_service.validate_video_size(update_data["video_file_path"]):
                raise ValueError("Video file is too large (max 100MB)")

            try:
                new_video_url = self.file_service.upload_video_file(
                    update_data["video_file_path"],
                    article_id
                )
                # Delete old video if it exists
                if video_url:
                    self.file_service.delete_video_file(video_url)
                video_url = new_video_url
            except Exception as e:
                raise RuntimeError(f"Failed to upload new video: {str(e)}")

        # Create update input with new URLs
        from ..domain.models import ArticleUpdateInput, ArticleCreationInput

        # Create a new article input with updated data
        updated_article_input = ArticleCreationInput(
            id=article_id,
            thumbnail_image_url=thumbnail_url,
            title=update_data.get("title", existing_article.title),
            subtitle=update_data.get("subtitle", existing_article.subtitle),
            video_file_url=video_url
        )

        # For now, we'll recreate the article since we don't have an update method in repository
        # In a real implementation, you'd want to add an update method to the repository
        try:
            # Delete the old article
            await self.article_repository.delete_article(article_id)
            # Create with updated data
            return await self.article_repository.create_article(updated_article_input)
        except Exception as e:
            raise RuntimeError(f"Failed to update article: {str(e)}")