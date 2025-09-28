from claude_code_sdk import tool, create_sdk_mcp_server, ClaudeSDKClient, ClaudeCodeOptions

"""MongoDB MCP Server for AITimes article management with Supabase image storage."""

from .Infrastructure.mongodb_client import MongoDBClient
from .Infrastructure.article_repository import ArticleRepository
from .service.image_upload_service import FileUploadService
from .service.article_service import ArticleService
from .domain.models import ArticleCreationRequest, article_creation_request_schema, article_update_input_schema

# Initialize services
mongo_client = MongoDBClient()
mongo_client.connect()
article_repository = ArticleRepository(mongo_client)
file_service = FileUploadService()
article_service = ArticleService(article_repository, file_service)


@tool(name="create_article", description="Create a new article with thumbnail and optional video upload to Supabase", input_schema=article_creation_request_schema)
async def create_article(args: dict):
    """Create a new article by uploading files to Supabase first."""
    try:
        request = ArticleCreationRequest(**args)
        article = await article_service.create_article_with_upload(request)

        return {
            "success": True,
            "article": {
                "id": article.id,
                "thumbnail_image_url": article.thumbnail_image_url,
                "video_file_url": article.video_file_url,
                "title": article.title,
                "subtitle": article.subtitle,
                "created_at": article.created_at.isoformat() if article.created_at else None
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool(name="get_article", description="Get an article by ID", input_schema={"type": "object", "properties": {"article_id": {"type": "string"}}, "required": ["article_id"]})
async def get_article(args: dict):
    """Get an article by ID."""
    try:
        article_id = args["article_id"]
        article = await article_service.get_article(article_id)

        return {
            "success": True,
            "article": {
                "id": article.id,
                "thumbnail_image_url": article.thumbnail_image_url,
                "video_file_url": article.video_file_url,
                "title": article.title,
                "subtitle": article.subtitle,
                "created_at": article.created_at.isoformat() if article.created_at else None,
                "updated_at": article.updated_at.isoformat() if article.updated_at else None
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@tool(name="update_article", description="Update an article by ID", input_schema=article_update_input_schema)
async def update_article(args: dict):
    """Update an article by ID."""
    try:
        article_id = args["id"]  # Changed from "article_id" to "id" to match schema
        article = await article_service.update_article(article_id, args)
        return {
            "success": True,
            "article": {
                "id": article.id,
                "thumbnail_image_url": article.thumbnail_image_url,
                "video_file_url": article.video_file_url,
                "title": article.title,
                "subtitle": article.subtitle,
                "created_at": article.created_at.isoformat() if article.created_at else None,
                "updated_at": article.updated_at.isoformat() if article.updated_at else None
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@tool(name="list_articles", description="List articles with pagination", input_schema={"type": "object", "properties": {"limit": {"type": "integer", "default": 100}, "offset": {"type": "integer", "default": 0}}})
async def list_articles(args: dict):
    """List articles with pagination."""
    try:
        limit = args.get("limit", 100)
        offset = args.get("offset", 0)
        articles = await article_service.list_articles(limit, offset)

        article_list = []
        for article in articles:
            article_list.append({
                "id": article.id,
                "thumbnail_image_url": article.thumbnail_image_url,
                "video_file_url": article.video_file_url,
                "title": article.title,
                "subtitle": article.subtitle,
                "created_at": article.created_at.isoformat() if article.created_at else None,
                "updated_at": article.updated_at.isoformat() if article.updated_at else None
            })

        return {
            "success": True,
            "articles": article_list,
            "count": len(article_list)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@tool(name="delete_article", description="Delete an article and its thumbnail", input_schema={"type": "object", "properties": {"article_id": {"type": "string"}}, "required": ["article_id"]})
async def delete_article(args: dict):
    """Delete an article and its thumbnail image."""
    try:
        article_id = args["article_id"]
        deleted = await article_service.delete_article(article_id)

        return {
            "success": deleted,
            "message": f"Article {'deleted' if deleted else 'not found'}: {article_id}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@tool(name="upload_video", description="Upload a video file to Supabase", input_schema={"type": "object", "properties": {"video_file_path": {"type": "string"}, "article_id": {"type": "string"}}, "required": ["video_file_path", "article_id"]})
async def upload_video(args: dict):
    """Upload a video file to Supabase."""
    try:
        video_file_path = args["video_file_path"]
        article_id = args["article_id"]
        video_url = file_service.upload_video_file(video_file_path, article_id)
        return {
            "success": True,
            "video_url": video_url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Create MCP server with tools
aitimes_db_mcp_server = create_sdk_mcp_server(
    name="aitimes-db-mcp",
    version="1.0.0",
    tools=[create_article, get_article, update_article, list_articles, delete_article, upload_video]
)