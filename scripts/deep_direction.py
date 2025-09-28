from typing import Any

import argparse
import re
from dotenv import load_dotenv
from typing import Any, Literal, Optional, List, Dict
from openai import OpenAI

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompts.prompts import DEEP_DIRECTION_PROMPT


load_dotenv()
client = OpenAI()

def create_file(file_path):
  with open(file_path, "rb") as file_content:
    result = client.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

def remove_analysis_tags(text: str) -> str:
    """
    Remove <analysis> tags and their content from the given text.
    """
    # Use regex to remove <analysis> tags and everything between them
    pattern = r'<analysis>.*?</analysis>'
    return re.sub(pattern, '', text, flags=re.DOTALL)


def reasoning(messages: List[Dict[str, Any]],reasoning_effort: Optional[str]="medium"):
    response = client.responses.create(
        model="gpt-5-mini",
        input=messages,
        reasoning={"effort": "minimal"}
    )
    return response.output_text


def deep_direction(article_id: str, article_path: str, article_image_url_or_paths: Optional[list[str]]=None):
    openai_image_ids = []
    if article_image_url_or_paths:
        for image_url in article_image_url_or_paths:
            image_id = create_file(f"{image_url}")
            openai_image_ids.append({
                "type": "input_image",
                "file_id": image_id
            })
    if article_path:
        article_content = open(article_path, "r").read()
    else:
        article_content = None
    
    user_content = [
        {
            "type": "input_text",
            "text": f"article_content: {article_content}"
        },
        *openai_image_ids
    ]
    
    messages = [
        {"role": "system", "content": DEEP_DIRECTION_PROMPT(article_content)},
        {"role": "user", "content": user_content}
    ]
    result = reasoning(messages)
    cleaned_result = remove_analysis_tags(result)
    with open(f"outputs/{article_id}_design_strategy.md", "w") as f:
        f.write(cleaned_result)
    return cleaned_result


def main():
    try:
        parser = argparse.ArgumentParser(description="Create Deep Direction Tool")
        parser.add_argument("--article_id", required=True, help="Article id")
        parser.add_argument("--article_path", required=True, help="Article path (resource/...)")
        parser.add_argument("--article_image_url_or_paths", nargs='+', required=True, help="Article image url or paths(resource/...)")
        args = parser.parse_args()
        result = deep_direction(args.article_id, args.article_path, args.article_image_url_or_paths)
        return result
    except Exception as e:
        print(e)
        return f"Error: {e}"

if __name__ == "__main__":
    exit(main())

