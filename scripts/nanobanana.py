#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

### Usage:
- Kawaii-style sticker with transparent background:
`python scripts/nanobanana.py --prompt "A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat. It's munching on a green bamboo leaf. The design features bold, clean outlines, simple cel-shading, and a vibrant color palette. The background must be white."`

- Product mockup with studio lighting:
`python scripts/nanobanana.py --prompt "A high-resolution, studio-lit product photograph of a minimalist ceramic coffee mug in matte black, presented on a polished concrete surface. The lighting is a three-point softbox setup designed to create soft, diffused highlights and eliminate harsh shadows. The camera angle is a slightly elevated 45-degree shot to showcase its clean lines. Ultra-realistic, with sharp focus on the steam rising from the coffee. Square image."`

- Style transfer:
`python scripts/nanobanana.py --prompt "Transform the provided photograph of a modern city street at night into the artistic style of Vincent van Gogh's 'Starry Night'. Preserve the original composition of buildings and cars, but render all elements with swirling, impasto brushstrokes and a dramatic palette of deep blues and bright yellows." --image "resource/city.png"`

- Combine multiple images for fashion e-commerce:
`python scripts/nanobanana.py --prompt "Create a professional e-commerce fashion photo. Take the blue floral dress from the first image and let the woman from the second image wear it. Generate a realistic, full-body shot of the woman wearing the dress, with the lighting and shadows adjusted to match the outdoor environment." --image "resource/dress.png" --image "resource/model.png"`

- Add logo to clothing with detail preservation:
`python scripts/nanobanana.py --prompt "Take the first image of the woman with brown hair, blue eyes, and a neutral expression. Add the logo from the second image onto her black t-shirt. Ensure the woman's face and features remain completely unchanged. The logo should look like it's naturally printed on the fabric, following the folds of the shirt." --image "resource/woman.png" --image "resource/logo.png"`

"""

import argparse
import io
import json
import mimetypes
import os
from datetime import datetime
from pathlib import Path
import requests
from urllib.parse import urlparse
from xai_sdk import Client
from PIL import Image
from dataclasses import dataclass

from google import genai
from google.genai import types

import os
from dotenv import load_dotenv
import sys

# Add creator_agent directory to Python path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
creator_agent_dir = os.path.dirname(script_dir)
if creator_agent_dir not in sys.path:
    sys.path.insert(0, creator_agent_dir)

load_dotenv()

def is_url(string: str) -> bool:
    """Check if a string is a valid URL."""
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_image_from_url(url: str) -> Image.Image:
    """Download an image from a URL and return a PIL Image object."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except Exception as e:
        raise RuntimeError(f"Failed to download image from URL: {e}")

def generate_or_edit(prompt: str, image_paths_or_urls: list = None, output_path: str = None) -> bytes:
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not found in environment variables.")

        client = genai.Client(api_key=api_key)

        # Handle image inputs - either URLs or local file paths
        contents = [prompt]

        if image_paths_or_urls:
            for image_path_or_url in image_paths_or_urls:
                if is_url(image_path_or_url):
                    print(f"📥 Downloading image from URL: {image_path_or_url}")
                    image = download_image_from_url(image_path_or_url)
                else:
                    print(f"📁 Loading local image: {image_path_or_url}")
                    image = Image.open(image_path_or_url)
                contents.append(image)

        response = client.models.generate_content(
            model="gemini-2.5-flash-image-preview",
            contents=contents,
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(io.BytesIO(part.inline_data.data))
                image.save(output_path)
                return output_path
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Google Gemini Image Generation/Editing Tool")
    parser.add_argument("--prompt", required=True, help="Generation/editing instruction text")
    parser.add_argument("--image", action='append', help="Source image path or URL for editing (can be used multiple times)", default=[])
    parser.add_argument("--output", help="Output file path", default=None)
    parser.add_argument("--size", default="1024x1024", help="Image size (for mock mode)")

    args = parser.parse_args()

    # Generate output path if not provided
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if args.image:
            args.output = f"outputs/edited_{timestamp}.png"
        else:
            args.output = f"outputs/generated_{timestamp}.png"

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    success = False
    error_msg = None

    try:
        # Use Google Gemini for image generation/editing
        img_data = generate_or_edit(prompt=args.prompt, image_paths_or_urls=args.image, output_path=args.output)
        print(f"✅ Image {'edited' if args.image else 'generated'} successfully!")
        print(f"📁 Output: {args.output}")
        success = True

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error: {error_msg}")
        success = False

    # Enhanced script execution logging
    command_parts = ["python", "scripts/nanobanana.py", f"--prompt", f'"{args.prompt}"']
    if args.image:
        for img in args.image:
            command_parts.extend(["--image", img])
    if args.output:
        command_parts.extend(["--output", args.output])

    full_command = " ".join(command_parts)

    # Keep original log format for backwards compatibility
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "tool": "nanobanana",
        "prompt": args.prompt,
        "image_inputs": args.image,
        "output_path": str(args.output),
        "size": args.size,
        "status": "success" if success else "error",
        "error": error_msg,
        "gemini_used": bool(os.getenv("GOOGLE_API_KEY"))
    }

    # Ensure logs directory exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Append to log file
    with open("logs/nanobanana.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    if success:
        print(f"🎨 Prompt: {args.prompt}")
        if args.image:
            print(f"🖼️ Sources: {', '.join(args.image)}")
        print(f"📊 Logged to: logs/nanobanana.log")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())