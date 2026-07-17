"""Chapter 09 — Your own Python function as a tool the agent can call.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
"""

import os

# Function calling: the agent asks, our code answers
import json
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]

project = AIProjectClient(endpoint=PROJECT_ENDPOINT,
                          credential=DefaultAzureCredential())

# 1) Describe the function with a JSON schema
get_device_status = {
    "type": "function",
    "name": "get_device_status",
    "description": "Return the compliance status of a managed device.",
    "parameters": {
        "type": "object",
        "properties": {
            "device_name": {"type": "string",
                            "description": "Device name as shown in Intune"}
        },
        "required": ["device_name"],
    },
}

agent = project.agents.create_version(
    agent_name="DeviceAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="You help IT admins. Use the tool to check devices.",
        tools=[get_device_status],
    ),
)

openai = project.get_openai_client(agent_name="DeviceAgent")
conversation = openai.conversations.create()
response = openai.responses.create(conversation=conversation.id,
                                   input="Is LAPTOP-JR42 compliant?")

# 2) The agent pauses with a function_call item; we execute and reply
for item in response.output:
    if item.type == "function_call":
        args = json.loads(item.arguments)
        result = {"device": args["device_name"], "compliant": True}  # real lookup here
        response = openai.responses.create(
            conversation=conversation.id,
            input=[{"type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(result)}],
        )

print(response.output_text)
