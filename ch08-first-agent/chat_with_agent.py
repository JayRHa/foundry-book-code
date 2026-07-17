"""Chapter 08 — Chatting with an agent that already exists.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

create_agent.py binds the client to one agent with get_openai_client(agent_name=...).
This is the other way round: an unbound client that names the agent per call, which is
what you want when one process talks to several agents.

Note the shape of agent_reference. `agent` on its own is deprecated and rejected, and
`type` is required inside the reference — the service reports those two problems one at
a time, so it is easy to fix the first and think you are done.

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
    export AGENT_NAME="MyAgent"
"""
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]
AGENT_NAME = os.environ.get("AGENT_NAME", "MyAgent")

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai = project.get_openai_client()  # no agent_name -> unbound

# Un-bound variant: reference the agent on each response call
response = openai.responses.create(
    extra_body={"agent_reference": {"name": AGENT_NAME, "type": "agent_reference"}},
    input="What is the size of France in square miles?",
)
print(response.output_text)
