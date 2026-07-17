# Create the private endpoint against the Foundry account subresource
az network private-endpoint create \
  --name pe-foundry-prod \
  --resource-group rg-ai-prod \
  --vnet-name vnet-spoke-ai --subnet snet-pe \
  --private-connection-resource-id "$FOUNDRY_ACCOUNT_ID" \
  --group-id account \
  --connection-name foundry-account
