"""Chapter 08 — Create an agent, then talk to it: agent, conversation, response.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
"""

import os

# Create an agent and chat with it (azure-ai-projects >= 2.x)
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,               # https://<resource>.services.ai.azure.com/api/projects/<project>
    credential=DefaultAzureCredential(),
)

# 1) Create (a version of) an agent — project client
agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-5.4-mini",                  # any Foundry direct model
        instructions="You are a helpful assistant that answers general questions",
    ),
)
print(agent.id, agent.name, agent.version)

# 2) Chat — OpenAI client (conversations + responses)
openai = project.get_openai_client(agent_name="MyAgent")  # pre-bound to the agent
conversation = openai.conversations.create()
r1 = openai.responses.create(conversation=conversation.id,
                             input="What is the size of France in square miles?")
print(r1.output_text)
r2 = openai.responses.create(conversation=conversation.id,
                             input="And what is the capital city?")
print(r2.output_text)
