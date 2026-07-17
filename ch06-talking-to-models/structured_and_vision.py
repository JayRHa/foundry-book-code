"""Chapter 06 — JSON-schema output and image input.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

Setup:
    az login
    export FOUNDRY_OPENAI_BASE_URL="https://<resource>.openai.azure.com/openai/v1/"
"""

# structured_and_vision.py — JSON-schema output and image input
import json
import os

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Same client as chat.py — see that file for what each argument is doing.
client = OpenAI(
    base_url=os.environ["FOUNDRY_OPENAI_BASE_URL"],
    api_key=get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    ),
)

# 1) Structured output: classify a raw Intune log line
schema = {
    "type": "object",
    "properties": {
        "error_code": {"type": "string"},
        "component": {"type": "string"},
        "severity": {"type": "string", "enum": ["low", "medium", "high"]},
    },
    "required": ["error_code", "component", "severity"],
    "additionalProperties": False,
}

completion = client.chat.completions.create(
    model="gpt-5.1-mini",
    messages=[
        {"role": "system", "content": "Extract the error details from the log line."},
        {"role": "user", "content": "Win32 app install failed on DEVICE-042 with 0x87D00668"},
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {"name": "intune_log_entry", "strict": True, "schema": schema},
    },
)
entry = json.loads(completion.choices[0].message.content)
print(entry["error_code"], entry["severity"])

# 2) Vision: send a screenshot to a multimodal deployment
response = client.chat.completions.create(
    model="gpt-5.1-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What error is shown in this screenshot, and what should I check first?"},
                # a public URL or a base64 data: URL both work
                {"type": "image_url", "image_url": {"url": "https://example.com/device-error.png"}},
            ],
        }
    ],
)
print(response.choices[0].message.content)
