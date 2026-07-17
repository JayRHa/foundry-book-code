az role assignment create \
  --assignee "<agentIdentityId>" \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/<sub-id>/resourceGroups/rg-ai-prod/providers/Microsoft.Storage/storageAccounts/stcontosodata"
