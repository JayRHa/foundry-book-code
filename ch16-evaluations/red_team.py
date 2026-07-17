"""Chapter 16 — Automated red teaming.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code

The listing in the book is written notebook-style, with a top-level `await`. As a file
it needs an event loop, so the same calls live inside `main()` here.

HEADS-UP (checked July 2026): `pip install "azure-ai-evaluation[redteam]"` currently
resolves to `pyrit==0.11.0`, which is no longer on PyPI, and pyrit 0.14 renamed the
`orchestrator` module to `executor` — so the extra does not install cleanly either way.
Until that is fixed, run the scan from the Foundry portal (Protect & govern -> Red
teaming). It does the same job and needs no local install.

Setup:
    az login
    export PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
"""
import asyncio
import os

from azure.identity import DefaultAzureCredential
from azure.ai.evaluation.red_team import RedTeam, RiskCategory, AttackStrategy

PROJECT_ENDPOINT = os.environ["PROJECT_ENDPOINT"]


async def my_agent_callback(query: str) -> str:
    """The thing under attack. Point this at your app, agent, or model endpoint.

    The scan calls it once per generated attack prompt and judges what comes back, so it
    must return the same text a real user would see — guardrails, system prompt and all.
    Return a stub here and you are red teaming the stub, not the agent.
    """
    raise NotImplementedError("Point this at your agent and return its answer as text.")


async def main() -> None:
    red_team = RedTeam(
        azure_ai_project=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(),
        risk_categories=[RiskCategory.Violence, RiskCategory.HateUnfairness],
    )
    result = await red_team.scan(
        target=my_agent_callback,
        attack_strategies=[AttackStrategy.Base64, AttackStrategy.Flip],
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
