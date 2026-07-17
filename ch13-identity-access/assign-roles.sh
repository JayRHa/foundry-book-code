# Assign Foundry User (GUID = rename-proof) to a developer at project scope
az role assignment create \
  --assignee "anna.developer@contoso.com" \
  --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-ai-prod/providers/Microsoft.CognitiveServices/accounts/foundry-contoso-prod/projects/proj-support-agents"

# Assign Foundry Agent Consumer to a service principal on ONE agent only
az role assignment create \
  --assignee "<sp-object-id>" \
  --role "eed3b665-ab3a-47b6-8f48-c9382fb1dad6" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-ai-prod/providers/Microsoft.CognitiveServices/accounts/foundry-contoso-prod/projects/proj-support-agents/agents/ticket-triage-agent"
