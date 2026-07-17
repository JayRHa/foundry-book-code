"""Chapter 09 — An OpenAPI spec as a tool.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

The appeal over function calling: you write no execution code at all. The service reads
the spec, picks the operation, calls it, and feeds the result back to the model. What
you give up is the chance to check anything in between — so anonymous auth, as used
here, belongs on public read-only APIs and nowhere else.

The book shows only the tool definition. The surrounding lines here are what it takes to
get that definition onto an agent.

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
    export OPENAPI_SPEC_PATH="./weather.json"
"""
import json
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (OpenApiTool,
    OpenApiFunctionDefinition, OpenApiAnonymousAuthDetails, PromptAgentDefinition)

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())

# The spec is the contract the agent reads. Any valid OpenAPI 3 document works.
with open(os.environ.get("OPENAPI_SPEC_PATH", "./weather.json")) as f:
    openapi_spec = json.load(f)

weather = OpenApiTool(openapi=OpenApiFunctionDefinition(
    name="get_weather", spec=openapi_spec,
    description="Retrieve weather information for a location.",
    auth=OpenApiAnonymousAuthDetails()))

agent = project.agents.create_version(
    agent_name="WeatherAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="Answer weather questions using the get_weather tool.",
        tools=[weather],
    ),
)
print(agent.name, agent.version)
