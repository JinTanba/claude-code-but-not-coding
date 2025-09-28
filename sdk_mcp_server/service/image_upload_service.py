"""File upload service that integrates local paths with Supabase storage for images and videos."""

import os
from typing import Optional

from ..Infrastructure.supabase_storage import SupabaseStorageClient


class FileUploadService:
    """Service for handling file uploads (images and videos) to Supabase storage."""

    def __init__(self, supabase_client: Optional[SupabaseStorageClient] = None):
        """Initialize file upload service."""
        self.supabase_client = supabase_client or SupabaseStorageClient()

    def upload_thumbnail_image(self, local_path: str, article_id: str) -> str:
        """
        Upload a thumbnail image to Supabase storage.

        Args:
            local_path: Local file path to the image
            article_id: Article ID for organizing files

        Returns:
            Public URL of the uploaded image

        Raises:
            FileNotFoundError: If the local image file doesn't exist
            ValueError: If the image format is unsupported
            RuntimeError: If upload fails
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Thumbnail image not found: {local_path}")

        # Use article_id as folder for better organization
        folder = f"thumbnails/{article_id}"

        try:
            public_url = self.supabase_client.upload_image(local_path, folder)
            print(f"Successfully uploaded thumbnail: {local_path} -> {public_url}")
            return public_url

        except Exception as e:
            raise RuntimeError(f"Failed to upload thumbnail image: {str(e)}")

    def upload_video_file(self, local_path: str, article_id: str) -> str:
        """
        Upload a video file to Supabase storage.

        Args:
            local_path: Local file path to the video
            article_id: Article ID for organizing files

        Returns:
            Public URL of the uploaded video

        Raises:
            FileNotFoundError: If the local video file doesn't exist
            ValueError: If the video format is unsupported
            RuntimeError: If upload fails
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Video file not found: {local_path}")

        # Use article_id as folder for better organization
        folder = f"videos/{article_id}"

        try:
            public_url = self.supabase_client.upload_video(local_path, folder)
            print(f"Successfully uploaded video: {local_path} -> {public_url}")
            return public_url

        except Exception as e:
            raise RuntimeError(f"Failed to upload video file: {str(e)}")

    def delete_thumbnail_image(self, public_url: str) -> bool:
        """
        Delete a thumbnail image from Supabase storage.

        Args:
            public_url: Public URL of the image to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        storage_path = self.supabase_client.extract_storage_path_from_url(public_url)
        if not storage_path:
            print(f"Could not extract storage path from URL: {public_url}")
            return False

        return self.supabase_client.delete_image(storage_path)

    def delete_video_file(self, public_url: str) -> bool:
        """
        Delete a video file from Supabase storage.

        Args:
            public_url: Public URL of the video to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        storage_path = self.supabase_client.extract_storage_path_from_url(public_url)
        if not storage_path:
            print(f"Could not extract storage path from URL: {public_url}")
            return False

        return self.supabase_client.delete_video(storage_path)

    def validate_image_path(self, local_path: str) -> bool:
        """
        Validate that the image path exists and is a supported format.

        Args:
            local_path: Local file path to validate

        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(local_path):
            return False

        supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        file_extension = os.path.splitext(local_path)[1].lower()

        return file_extension in supported_extensions

    def validate_video_path(self, local_path: str) -> bool:
        """
        Validate that the video path exists and is a supported format.

        Args:
            local_path: Local file path to validate

        Returns:
            True if valid, False otherwise
        """
        if not os.path.exists(local_path):
            return False

        supported_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v']
        file_extension = os.path.splitext(local_path)[1].lower()

        return file_extension in supported_extensions

    def get_file_size_mb(self, local_path: str) -> float:
        """
        Get the size of a file in MB.

        Args:
            local_path: Local file path

        Returns:
            File size in MB
        """
        if not os.path.exists(local_path):
            return 0.0

        size_bytes = os.path.getsize(local_path)
        return size_bytes / (1024 * 1024)

    def validate_file_size(self, local_path: str, max_size_mb: float = 100.0) -> bool:
        """
        Validate that the file size is within limits.

        Args:
            local_path: Local file path
            max_size_mb: Maximum allowed size in MB (default 100MB for videos)

        Returns:
            True if size is acceptable, False otherwise
        """
        size_mb = self.get_file_size_mb(local_path)
        return size_mb <= max_size_mb

    def validate_image_size(self, local_path: str, max_size_mb: float = 10.0) -> bool:
        """
        Validate that the image size is within limits.

        Args:
            local_path: Local file path
            max_size_mb: Maximum allowed size in MB

        Returns:
            True if size is acceptable, False otherwise
        """
        size_mb = self.get_file_size_mb(local_path)
        return size_mb <= max_size_mb

    def validate_video_size(self, local_path: str, max_size_mb: float = 100.0) -> bool:
        """
        Validate that the video size is within limits.

        Args:
            local_path: Local file path
            max_size_mb: Maximum allowed size in MB

        Returns:
            True if size is acceptable, False otherwise
        """
        size_mb = self.get_file_size_mb(local_path)
        return size_mb <= max_size_mb