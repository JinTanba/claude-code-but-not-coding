---
name: prcreative
description: Create titles, subtitles, and thumbnail images to make published articles go viral.
---
Using scripts/deep_direction.py and graphic-designer, perform creative direction and generate thumbnail images for all articles in /input.json.
- Execute asynchronously in parallel to improve efficiency.
- Running scripts/deep_direction.py may take some time, so you will need to wait until it completes.

## output schema
```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Output",
  "type": "array",
  "items": {
    "type": "object",
    "title": "Article",
    "properties": {
      "id": {
        "type": "string",
        "description": "記事を一意に識別するID"
      },
      "thambnail_image_html_screenshot_path": {
        "type": "string",
        "description": "サムネイル画像スクショパス"
      },
      "title": {
        "type": "string",
        "description": "記事のタイトル"
      },
      "subtitle": {
        "type": "string",
        "description": "記事のサブタイトル"
      },
      "video_file_path": {
        "type": "string",
        "description": "生成したビデオのファイルのパス"
      }
    },
    "required": [
      "id",
      "thambnail_image_html_screenshot_path",
      "title",
      "subtitle"
    ],
    "additionalProperties": false
  }
}
```

Please note that graphic-designer must create thumbnail images based on the decisions made by scripts/deep_direction.py


NOTE:
- If you already have clear design instructions, simply pass them on to the Agent. Do not add anything further regarding the design requirements.
- Running scripts/deep_direction.py may take some time, so you will need to wait until it completes.
- Please organize all final outputs and append them to the outputs/ directory.