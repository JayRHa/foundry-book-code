"""Chapter 16 — Evaluate an agent with the azure-ai-evaluation SDK.

From the book "Microsoft Foundry" by Jannik Reinhard.
https://github.com/JayRHa/foundry-book-code
"""

# pip install azure-ai-evaluation azure-identity  (az login first — Entra ID is required)
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import (
    evaluate, GroundednessEvaluator, RelevanceEvaluator,
    TaskAdherenceEvaluator, ToolCallAccuracyEvaluator,
)

# Judge model used by the AI-assisted evaluators
model_config = {
    "azure_endpoint": "https://<your-resource>.openai.azure.com",
    "azure_deployment": "gpt-4.1-mini",
}

result = evaluate(
    data="eval-dataset.jsonl",  # one test case per line: query, context, response, ...
    evaluators={
        "groundedness": GroundednessEvaluator(model_config=model_config),
        "relevance": RelevanceEvaluator(model_config=model_config),
        "task_adherence": TaskAdherenceEvaluator(model_config=model_config),
        "tool_call_accuracy": ToolCallAccuracyEvaluator(model_config=model_config),
    },
    # Log the run into your Foundry project (visible in the portal)
    azure_ai_project="https://<your-resource>.services.ai.azure.com/api/projects/<project>",
)
print(result["metrics"])  # aggregate scores, e.g. groundedness pass rate
