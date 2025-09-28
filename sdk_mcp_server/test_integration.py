#!/usr/bin/env python3
"""Integration test script for MongoDB + Supabase setup."""

import asyncio
import os
import tempfile
from PIL import Image
from dotenv import load_dotenv

from Infrastructure.mongodb_client import MongoDBClient
from Infrastructure.article_repository import ArticleRepository
from service.image_upload_service import FileUploadService
from service.article_service import ArticleService
from domain.models import ArticleCreationRequest

# Load environment variables
load_dotenv()

async def test_integration():
    """Test the complete integration."""
    print("🧪 Testing MongoDB + Supabase Integration...")

    # Check environment variables
    print("\n📋 Environment Variables:")
    print(f"MONGODB_URL: {'✓' if os.getenv('MONGODB_URL') else '✗ Missing'}")
    print(f"MONGODB_DATABASE: {os.getenv('MONGODB_DATABASE', 'Not set')}")
    print(f"SUPABASE_URL: {'✓' if os.getenv('SUPABASE_URL') else '✗ Missing'}")
    print(f"SUPABASE_KEY: {'✓' if os.getenv('SUPABASE_KEY') else '✗ Missing'}")
    print(f"SUPABASE_BUCKET_NAME: {os.getenv('SUPABASE_BUCKET_NAME', 'Not set')}")

    # Test MongoDB connection
    print("\n🍃 Testing MongoDB Connection...")
    try:
        mongo_client = MongoDBClient()
        mongo_client.connect()
        print("✅ MongoDB connection successful")

        # Test article repository
        article_repo = ArticleRepository(mongo_client)
        article_repo.create_indexes()
        print("✅ MongoDB indexes created")

    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return

    # Test Supabase connection
    print("\n☁️ Testing Supabase Connection...")
    try:
        file_service = FileUploadService()
        print("✅ Supabase client initialized")

    except Exception as e:
        print(f"❌ Supabase initialization failed: {e}")
        return

    # Create test image
    print("\n🖼️ Creating test image...")
    try:
        # Create a simple test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            # Create a simple 100x100 red image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(temp_file.name, 'PNG')
            test_image_path = temp_file.name

        print(f"✅ Test image created: {test_image_path}")

        # Test image validation
        if file_service.validate_image_path(test_image_path):
            print("✅ Image validation passed")
        else:
            print("❌ Image validation failed")
            return

    except Exception as e:
        print(f"❌ Test image creation failed: {e}")
        return

    # Test complete article creation flow
    print("\n📝 Testing Article Creation Flow...")
    try:
        article_service = ArticleService(article_repo, file_service)

        # Create test article
        test_request = ArticleCreationRequest(
            id=f"test-article-{int(asyncio.get_event_loop().time())}",
            thumbnail_image_path=test_image_path,
            title="Test Article Title",
            subtitle="Test Article Subtitle"
        )

        # Create article (this will upload image and save to DB)
        created_article = await article_service.create_article_with_upload(test_request)

        print(f"✅ Article created successfully!")
        print(f"   ID: {created_article.id}")
        print(f"   Thumbnail URL: {created_article.thumbnail_image_url}")
        print(f"   Title: {created_article.title}")

        # Test retrieval
        retrieved_article = await article_service.get_article(created_article.id)
        print(f"✅ Article retrieved successfully: {retrieved_article.title}")

        # Test listing
        articles = await article_service.list_articles(limit=5)
        print(f"✅ Articles listed: {len(articles)} found")

        # Clean up test article
        deleted = await article_service.delete_article(created_article.id)
        if deleted:
            print("✅ Test article deleted (cleanup successful)")
        else:
            print("⚠️ Test article deletion failed (manual cleanup may be needed)")

    except Exception as e:
        print(f"❌ Article creation flow failed: {e}")
        import traceback
        traceback.print_exc()
        return

    finally:
        # Clean up test image
        try:
            os.unlink(test_image_path)
            print("✅ Test image file cleaned up")
        except:
            pass

        # Close MongoDB connection
        mongo_client.disconnect()
        print("✅ MongoDB connection closed")

    print("\n🎉 Integration test completed successfully!")
    print("Your MongoDB + Supabase setup is working correctly.")

if __name__ == "__main__":
    asyncio.run(test_integration())