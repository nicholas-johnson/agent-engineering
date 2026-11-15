# Vision — ask a multimodal model to describe every image in playground/vision/images/.
# Run from the module folder: uv run python playground/vision/play.py
#                         or: source ../../.venv/bin/activate && python playground/vision/play.py
#
# To play: drop your own PNG/JPEG/WebP/GIF files into images/, change QUESTION below,
# or add "detail": "low" / "high" to the input_image dict (see README.md).

import base64
import mimetypes
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

HERE = Path(__file__).parent
OUTPUT = HERE / "output"
OUTPUT.mkdir(exist_ok=True)

MODEL = "gpt-6-luna"
QUESTION = "Describe this picture in two sentences."

client = OpenAI()
descriptions = []

# Encode each image in images/ as a base64 data URL and send it alongside QUESTION.
for image in sorted((HERE / "images").iterdir()):
    mime_type = mimetypes.guess_type(image.name)[0]
    if mime_type not in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        continue

    encoded = base64.b64encode(image.read_bytes()).decode()
    response = client.responses.create(
        model=MODEL,
        reasoning={"effort": "none"},
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": QUESTION},
                    {"type": "input_image", "image_url": f"data:{mime_type};base64,{encoded}"},
                ],
            }
        ],
    )

    print(f"=== {image.name} ===\n{response.output_text}\n")
    descriptions.append(f"=== {image.name} ===\n{response.output_text}\n")

(OUTPUT / "descriptions.txt").write_text("\n".join(descriptions))
