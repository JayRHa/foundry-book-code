"""Chapter 21 — Code against the local endpoint — the same OpenAI client, a different base URL.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code
"""

# Same OpenAI SDK as in Chapter 6 — only the base_url changes.
# Get the port from: foundry service status
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:<port>/v1",  # local Foundry Local server
    api_key="not-needed-locally"            # no key required on-device
)

response = client.chat.completions.create(
    model="qwen2.5-0.5b",
    messages=[{"role": "user", "content": "Summarize why local inference helps with privacy."}],
    stream=True,
)
for chunk in response:
    if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
