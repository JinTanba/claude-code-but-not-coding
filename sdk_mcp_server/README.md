# AITimes MongoDB + Supabase MCP Server

A MongoDB Atlas + Supabase integration server for AITimes autonomous agent to store article data with thumbnail images uploaded to Supabase storage.

## Features

- **Clean Architecture**: Separated domain models, infrastructure, and service layers
- **MongoDB Atlas Integration**: Robust connection handling with proper error management
- **Supabase Storage**: Automatic thumbnail image upload to Supabase with public URLs
- **Article Management**: Full CRUD operations for article data
- **Image Processing**: Automatic image validation, upload, and cleanup
- **MCP Server Tools**: Ready-to-use tools for Claude Code SDK integration
- **Data Validation**: Comprehensive input validation and error handling
- **Async Support**: Full async/await support for high performance

## Architecture

```
sdk_mcp_server/
├── domain/
│   └── models.py           # Domain models (Article, ArticleCreationInput, etc.)
├── Infrastructure/
│   ├── mongodb_client.py   # MongoDB Atlas connection management
│   └── article_repository.py # Database operations
├── service/
│   └── article_service.py  # Business logic layer
├── tests/
│   ├── test_models.py      # Domain model tests
│   └── test_article_service.py # Service layer tests
└── server.py               # MCP server implementation
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB Atlas & Supabase

1. **Create a MongoDB Atlas cluster** and get your connection string
2. **Create a Supabase project** and get your URL and anonymous key
3. **Create a Supabase storage bucket** named `aitimes-thumbnails` (or your preferred name)
4. Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:
```env
# MongoDB Atlas Configuration
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/database?retryWrites=true&w=majority&appName=Cluster0
MONGODB_DATABASE=your_database_name

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_BUCKET_NAME=your-bucket-name
```

### 3. Initialize Database

The server will automatically create necessary indexes when first started.

## Usage

### As MCP Server

```python
from sdk_mcp_server.server import create_server

server = create_server()
# Server will be available as MCP tools
```

### Programmatic Usage

```python
import asyncio
from sdk_mcp_server.server import AITimesMongoDBServer

async def main():
    server = AITimesMongoDBServer()
    await server.initialize()

    # Create article
    article_data = {
        "id": "article-1",
        "thumbnail_image_html_screenshot_path": "/path/to/thumbnail.png",
        "title": "Viral Article Title",
        "subtitle": "Engaging Subtitle"
    }

    result = await server.create_article(article_data)
    print(f"Created article: {result['id']}")

    await server.cleanup()

asyncio.run(main())
```

### Import from prcreative Output

```python
# Import articles from JSON file created by prcreative command
results = await server.bulk_create_articles_from_json("/path/to/outputs/articles.json")
print(f"Imported {len(results)} articles")
```

## MCP Tools Available

1. **create_article**: Create an article with automatic thumbnail upload to Supabase
2. **get_article**: Retrieve article by ID with Supabase image URL
3. **list_articles**: List articles with pagination
4. **delete_article**: Delete article and its thumbnail from both MongoDB and Supabase

## Data Schema

Articles are stored with the following structure:

```json
{
  "id": "unique-article-id",
  "thumbnail_image_url": "https://supabase.co/storage/v1/object/public/bucket/thumbnails/uuid.png",
  "title": "Article Title",
  "subtitle": "Article Subtitle",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Input Schema

When creating articles, provide a local image path that will be automatically uploaded:

```json
{
  "id": "unique-article-id",
  "thumbnail_image_path": "/local/path/to/screenshot.png",
  "title": "Article Title",
  "subtitle": "Article Subtitle"
}
```

## Testing

Run tests:

```bash
python -m unittest discover tests/
```

## Integration with prcreative

This server is designed to work seamlessly with the `/prcreative` command output format:

```json
[
  {
    "id": "article-1",
    "thambnail_image_html_screenshot_path": "/path/to/screenshot.png",
    "title": "Viral Title",
    "subtitle": "Engaging Subtitle"
  }
]
```

Note: The typo "thambnail" in the original schema is handled automatically.

## Error Handling

- **Connection Errors**: Automatic retry and proper error messages
- **Validation Errors**: Comprehensive input validation with clear error messages
- **Duplicate IDs**: Proper handling of duplicate article IDs
- **Resource Cleanup**: Automatic cleanup of database connections

## Performance Considerations

- **Async Operations**: All database operations are async
- **Connection Pooling**: MongoDB client handles connection pooling automatically
- **Indexed Queries**: Proper indexes on ID and created_at fields
- **Bulk Operations**: Efficient bulk insertion for multiple articles