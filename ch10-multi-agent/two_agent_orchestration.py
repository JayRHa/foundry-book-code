"""Chapter 10 — A two-agent orchestration: a researcher and a writer.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
"""

# Sequential two-agent workflow with the Microsoft Agent Framework
import asyncio
from agent_framework import SequentialBuilder
from agent_framework_foundry import FoundryChatClient
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = "https://<resource>.services.ai.azure.com/api/projects/<project>"

async def main():
    # One chat client against the model deployment from Chapter 5
    client = FoundryChatClient(
        endpoint=PROJECT_ENDPOINT,
        model="gpt-5-mini",
        credential=DefaultAzureCredential(),
    )

    researcher = client.create_agent(
        name="researcher",
        instructions="Collect the key facts on the topic as a short bullet list.",
    )
    writer = client.create_agent(
        name="writer",
        instructions="Turn the bullet list you receive into a short, "
                     "friendly summary for IT admins.",
    )

    # Researcher runs first, its output becomes the writer's input
    workflow = SequentialBuilder().participants([researcher, writer]).build()

    result = await workflow.run("What is the Model Context Protocol?")
    print(result.get_outputs()[-1])

asyncio.run(main())
