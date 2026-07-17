"""Chapter 12 — Image and video generation.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code
"""

# Generate an image with a gpt-image-2 deployment via the OpenAI v1 endpoint
import base64, os
from openai import OpenAI

client = OpenAI(
    base_url="https://<resource>.openai.azure.com/openai/v1/",
    api_key=os.environ["FOUNDRY_API_KEY"],  # Entra ID is the better option, see chapter 13
)

result = client.images.generate(
    model="gpt-image-2",  # your deployment name
    prompt="A clean line-art diagram of a phone-support agent, white background",
    size="1024x1024",
)

with open("agent-hero.png", "wb") as f:
    f.write(base64.b64decode(result.data[0].b64_json))
