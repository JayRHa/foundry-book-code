"""Chapter 07 — Query a Foundry IQ knowledge base from code.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code
"""

# pip install "azure-ai-projects>=2.0.0"  (Projects 2.x — 1.x is incompatible)
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

project = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential())

agent = project.agents.create_version(
    agent_name="kb-agent",
    definition=PromptAgentDefinition(
        model="gpt-4.1-mini",
        instructions="Answer only from the knowledge base and cite sources. "
                     "If you find nothing, say you don't know.",
        tools=[MCPTool(
            server_label="knowledge-base",
            server_url="https://<search>.search.windows.net/knowledgebases/"
                       "<kb-name>/mcp?api-version=2026-05-01-preview",
            allowed_tools=["knowledge_base_retrieve"],
            project_connection_id="<remote-tool-connection-id>")]))

openai = project.get_openai_client()
resp = openai.responses.create(
    input="What does our warranty cover for water damage?",
    extra_body={"agent_reference": {"name": agent.name,
                                    "type": "agent_reference"}})
print(resp.output_text)
