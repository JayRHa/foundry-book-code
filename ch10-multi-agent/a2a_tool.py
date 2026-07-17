"""Chapter 10 — One agent calling another with the A2A tool (public preview).

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

A2A points an agent at an agent somewhere else — another project, another team, another
vendor. The remote agent is reached through a project connection, so `conn` below is the
connection you created for it, not the agent itself. Create it once in the portal
(Management center -> Connections) or with the CLI, then look it up by name as here.

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
    export A2A_CONNECTION_NAME="network-specialist"
"""
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import A2APreviewTool, PromptAgentDefinition

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

# The connection that points at the remote agent.
conn = project.connections.get(name=os.environ["A2A_CONNECTION_NAME"])

# Attach a remote A2A agent as a tool (public preview)
agent = project.agents.create_version(
    agent_name="dispatcher",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="Route network questions to the network specialist agent.",
        tools=[A2APreviewTool(project_connection_id=conn.id)],
    ),
)
print(agent.name, agent.version)
