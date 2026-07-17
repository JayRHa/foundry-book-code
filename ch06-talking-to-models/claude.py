"""Chapter 06 — Calling Claude on Foundry through the native Anthropic Messages API.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code
"""

# claude.py — native Anthropic Messages API on Foundry
import os
from anthropic import Anthropic

claude = Anthropic(
    base_url="https://my-foundry-resource.services.ai.azure.com/anthropic",
    api_key=os.environ["FOUNDRY_API_KEY"],
)

message = claude.messages.create(
    model="claude-sonnet-5",   # must be deployed on the resource first
    max_tokens=1024,           # required by the Messages API
    messages=[
        {"role": "user", "content": "Compare Intune compliance policies and configuration profiles in three sentences."}
    ],
)
print(message.content[0].text)
