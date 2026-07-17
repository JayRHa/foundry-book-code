"""Chapter 09 — An MCP server as a tool.

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

# Attach a remote MCP server to an agent
from azure.ai.projects.models import MCPTool, PromptAgentDefinition

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]

github_tool = MCPTool(
    server_label="github",
    server_url="https://api.githubcopilot.com/mcp",
    require_approval="always",              # human approves each call
    project_connection_id="my-github-connection",
)

agent = project.agents.create_version(
    agent_name="DevAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You help with GitHub repository questions.",
        tools=[github_tool],
    ),
)
