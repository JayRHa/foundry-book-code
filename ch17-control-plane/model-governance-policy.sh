# Look up the built-in definition by its display name
defName=$(az policy definition list \
  --query "[?displayName=='Foundry model deployments should only use approved models'].name" -o tsv)

# Assign it with Deny effect; trailing slash pins gpt-5 exactly
az policy assignment create \
  --name "prod-approved-models" \
  --display-name "Prod: only approved Foundry models" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-ai-prod" \
  --policy "$defName" \
  --params '{
    "effect": { "value": "Deny" },
    "allowedPublishers": { "value": ["OpenAI"] },
    "allowedAssetIds": { "value": ["azureml://registries/azure-openai/models/gpt-5/"] }
  }'
