"""Chapter 12 — Wiring Foundry Tools into an agent.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code
"""

# Give an agent a Foundry Tool (Translator) as a custom function tool
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

project = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential(),
)

translate_tool = {
    "type": "function",
    "name": "translate_text",
    "description": "Translate text into a target language using the Translator tool.",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "target_language": {"type": "string", "description": "e.g. 'de' or 'fr'"},
        },
        "required": ["text", "target_language"],
    },
}

agent = project.agents.create_version(
    agent_name="support-translator",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions="Answer support questions. When the user asks for another "
                     "language, call translate_text instead of translating yourself.",
        tools=[translate_tool],
    ),
)
