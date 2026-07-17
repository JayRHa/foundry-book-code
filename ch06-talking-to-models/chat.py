"""Chapter 06 — First chat completion and streaming against the v1 endpoint, with Entra auth.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

Setup:
    az login
    export FOUNDRY_OPENAI_BASE_URL="https://<resource>.openai.azure.com/openai/v1/"
"""

# chat.py — first chat completion + streaming against the Foundry v1 endpoint
import os

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    # The book prints this as https://<resource>.openai.azure.com/openai/v1/ — it is an
    # environment variable here so the file runs against your resource, not the book's.
    base_url=os.environ["FOUNDRY_OPENAI_BASE_URL"],
    api_key=token_provider,  # a key string would also work here
)

# 1) Simple chat completion
completion = client.chat.completions.create(
    model="gpt-5.1-mini",  # your DEPLOYMENT name
    messages=[
        {"role": "system", "content": "You are a helpful IT admin assistant."},
        {"role": "user", "content": "Explain in two sentences what Microsoft Intune does."},
    ],
)
print(completion.choices[0].message.content)
print(completion.usage)  # prompt, completion, and total tokens

# 2) The same call, streamed token by token
stream = client.chat.completions.create(
    model="gpt-5.1-mini",
    messages=[{"role": "user", "content": "Write a short haiku about device compliance."}],
    stream=True,
)
for chunk in stream:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
