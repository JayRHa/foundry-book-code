"""Chapter 10 — Agent memory (preview): what the agent remembers between conversations.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
"""

import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

# Attach a per-user memory store to an agent (preview)
from azure.ai.projects.models import MemorySearchPreviewTool, PromptAgentDefinition

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]

tool = MemorySearchPreviewTool(
    memory_store_name="support-memory",
    scope="{{$userId}}",
    update_delay=300,   # seconds to wait before distilling new memories
)
agent = project.agents.create_version(
    agent_name="support-agent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="Use memory to recall the user's environment and past tickets.",
        tools=[tool],
    ),
)
