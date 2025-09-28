import argparse
import time
from google import genai

client = genai.Client()

def generate_video(prompt: str, output_path: str):
    operation = client.models.generate_videos(
        model="veo-3.0-generate-001",
        prompt=prompt,
    )

    # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    # Download the generated video.
    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(output_path)

def main():
    parser = argparse.ArgumentParser(description="Google Gemini Image Generation/Editing Tool")
    parser.add_argument("--prompt", required=True, help="video generation instruction text")
    parser.add_argument("--output_path", required=True, help="Output file path")
    args = parser.parse_args()
    generate_video(args.prompt, args.output_path)

if __name__ == "__main__":
    main()

