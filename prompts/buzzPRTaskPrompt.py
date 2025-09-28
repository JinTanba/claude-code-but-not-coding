import asyncio
from typing import Any, Dict, Generator

double_check_prompt = """
/video_creation
"""

display_all_thambnail_images_prompt = """
TODO:
1. Open the image file and show the user the image you created.
2. save the image to the database. You will save it to the database using MCP.
"""

def create_buzz_pr_task_prompt():
    async def message_generator():
        # 最初のメッセージ
        yield {
            "type": "user",
            "message": {
                "role": "user",
                "content": "/prcreative"
            }
        }

        # 条件を待機
        await asyncio.sleep(20)

        # 四番目のメッセージ
        yield {
            "type": "user",
            "message": {
                "role": "user",
                "content": display_all_thambnail_images_prompt
            }
        }
        await asyncio.sleep(20)

    return message_generator