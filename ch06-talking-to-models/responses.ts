// responses.ts — Foundry SDK for TypeScript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const project = new AIProjectClient(
  "https://my-foundry-resource.services.ai.azure.com/api/projects/my-foundry-project",
  new DefaultAzureCredential()
);

const openai = await project.getOpenAIClient();
const response = await openai.responses.create({
  model: "gpt-5.1-mini",
  input: "List three common causes of Intune enrollment failures.",
});
console.log(response.output_text);
