"""Chapter 15 — Catch a content-filter block and tell the user something true.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

The three cases this separates are the whole point: a blocked prompt (HTTP 400), a
blocked completion (HTTP 200 with finish_reason=content_filter), and filters that did
not run at all. They are not the same event and must not share an error message.

Setup:
    az login
    export FOUNDRY_OPENAI_BASE_URL="https://<resource>.openai.azure.com/openai/v1/"
"""

# Handle guardrail events on a chat completion call
import logging
import os
import sys

from openai import BadRequestError, OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = OpenAI(
    base_url=os.environ["FOUNDRY_OPENAI_BASE_URL"],
    api_key=get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    ),
)

user_input = " ".join(sys.argv[1:]) or "Explain in two sentences what Microsoft Intune does."

try:
    response = client.chat.completions.create(
        model="my-deployment",
        messages=[{"role": "user", "content": user_input}],
    )
    choice = response.choices[0]

    if choice.finish_reason == "content_filter":
        # Completion was blocked by the output pipeline (HTTP 200)
        print("The answer was blocked by our safety rules.")
    else:
        # Verify the filters actually ran (outage check)
        results = getattr(choice, "content_filter_results", None) or {}
        if "content_filter_error" in results:
            log.warning("Guardrails did not run for this response.")
        print(choice.message.content)

except BadRequestError as e:
    if getattr(e, "code", None) == "content_filter":
        # Prompt was blocked by the input pipeline (HTTP 400)
        print("Your request was blocked by our safety rules.")
    else:
        raise
