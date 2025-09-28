"""Supabase storage client for image uploads."""

import os
import uuid
from typing import Optional
from pathlib import Path

from supabase import create_client, Client

from dotenv import load_dotenv

load_dotenv()

class SupabaseStorageClient:
    """Client for Supabase storage operations."""

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None, bucket_name: Optional[str] = None):
        """Initialize Supabase storage client."""
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")  # Updated to match actual env var
        self.bucket_name = bucket_name or os.getenv("SUPABASE_BUCKET_NAME", "article")

        if not self.url or not self.key:
            raise ValueError("Supabase URL and anonymous key are required")

        self.client: Client = create_client(self.url, self.key)

    def upload_image(self, local_path: str, folder: str = "thumbnails") -> str:
        """
        Upload an image to Supabase storage and return the public URL.

        Args:
            local_path: Local file path to the image
            folder: Folder in the bucket to store the image

        Returns:
            Public URL of the uploaded image
        """
        return self._upload_file(local_path, folder, "image")

    def upload_video(self, local_path: str, folder: str = "videos") -> str:
        """
        Upload a video to Supabase storage and return the public URL.

        Args:
            local_path: Local file path to the video
            folder: Folder in the bucket to store the video

        Returns:
            Public URL of the uploaded video
        """
        return self._upload_file(local_path, folder, "video")

    def _upload_file(self, local_path: str, folder: str, file_type: str) -> str:
        """
        Upload a file to Supabase storage and return the public URL.

        Args:
            local_path: Local file path to the file
            folder: Folder in the bucket to store the file
            file_type: Type of file ("image" or "video")

        Returns:
            Public URL of the uploaded file
        """
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"{file_type.capitalize()} file not found: {local_path}")

        # Generate unique filename
        file_extension = Path(local_path).suffix.lower()

        # Validate file extension based on type
        if file_type == "image":
            supported_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
        elif file_type == "video":
            supported_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v']
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        if file_extension not in supported_extensions:
            raise ValueError(f"Unsupported {file_type} format: {file_extension}")

        unique_filename = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"{folder}/{unique_filename}"

        try:
            # Read the file
            with open(local_path, 'rb') as file:
                file_data = file.read()

            # Upload to Supabase storage
            response = self.client.storage.from_(self.bucket_name).upload(
                path=storage_path,
                file=file_data,
                file_options={"content-type": self._get_content_type(file_extension)}
            )

            if response.status_code not in [200, 201]:
                raise RuntimeError(f"Failed to upload {file_type}: {response}")

            # Get public URL
            public_url = self.client.storage.from_(self.bucket_name).get_public_url(storage_path)

            return public_url

        except Exception as e:
            raise RuntimeError(f"Error uploading {file_type} to Supabase: {str(e)}")

    def delete_image(self, storage_path: str) -> bool:
        """
        Delete an image from Supabase storage.

        Args:
            storage_path: Path in storage (e.g., "thumbnails/uuid.png")

        Returns:
            True if successful, False otherwise
        """
        return self._delete_file(storage_path, "image")

    def delete_video(self, storage_path: str) -> bool:
        """
        Delete a video from Supabase storage.

        Args:
            storage_path: Path in storage (e.g., "videos/uuid.mp4")

        Returns:
            True if successful, False otherwise
        """
        return self._delete_file(storage_path, "video")

    def _delete_file(self, storage_path: str, file_type: str) -> bool:
        """
        Delete a file from Supabase storage.

        Args:
            storage_path: Path in storage
            file_type: Type of file for logging

        Returns:
            True if successful, False otherwise
        """
        try:
            response = self.client.storage.from_(self.bucket_name).remove([storage_path])
            return response.status_code == 200
        except Exception as e:
            print(f"Error deleting {file_type} from Supabase: {str(e)}")
            return False

    def _get_content_type(self, file_extension: str) -> str:
        """Get MIME type for file extension."""
        content_types = {
            # Image types
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp',

            # Video types
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime',
            '.avi': 'video/x-msvideo',
            '.mkv': 'video/x-matroska',
            '.webm': 'video/webm',
            '.m4v': 'video/x-m4v'
        }
        return content_types.get(file_extension.lower(), 'application/octet-stream')

    def get_url_from_path(self, storage_path: str) -> str:
        """Get public URL from storage path."""
        return self.client.storage.from_(self.bucket_name).get_public_url(storage_path)

    def extract_storage_path_from_url(self, public_url: str) -> Optional[str]:
        """Extract storage path from public URL for deletion."""
        try:
            # URL format: https://xxx.supabase.co/storage/v1/object/public/bucket/path
            url_parts = public_url.split(f"/object/public/{self.bucket_name}/")
            if len(url_parts) == 2:
                return url_parts[1]
            return None
        except Exception:
            return None