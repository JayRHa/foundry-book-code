"""Call a Claude deployment in Foundry using Microsoft Entra ID.

Set FOUNDRY_ANTHROPIC_ENDPOINT to https://<resource>.services.ai.azure.com/anthropic
and FOUNDRY_CLAUDE_DEPLOYMENT to an existing Claude deployment.
"""
import os
from anthropic import AnthropicFoundry
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def main():
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(), "https://ai.azure.com/.default"
    )
    with AnthropicFoundry(
        base_url=os.environ["FOUNDRY_ANTHROPIC_ENDPOINT"],
        azure_ad_token_provider=token_provider,
    ) as client:
        message = client.messages.create(
            model=os.environ["FOUNDRY_CLAUDE_DEPLOYMENT"],
            max_tokens=1024,
            messages=[{"role": "user", "content":
                       "Compare Intune compliance policies and configuration profiles."}],
        )
        for block in message.content:
            if block.type == "text":
                print(block.text)

if __name__ == "__main__":
    main()
