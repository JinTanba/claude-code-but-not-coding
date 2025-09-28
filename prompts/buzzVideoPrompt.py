import asyncio
from typing import Any, Dict, Generator

create_video_prompt = """
/video_creation
"""

display_all_video_prompt = """
TODO:
1. Open and show me the video you created.
2. save the video to the database. You will save it to the database using MCP.
"""

def create_buzz_video_prompt():
    async def message_generator():
        # 最初のメッセージ
        yield {
            "type": "user",
            "message": {
                "role": "user",
                "content": create_video_prompt
            }
        }

        # 条件を待機
        await asyncio.sleep(20)

        # 四番目のメッセージ
        yield {
            "type": "user",
            "message": {
                "role": "user",
                "content": display_all_video_prompt
            }
        }
        await asyncio.sleep(20)

    return message_generator