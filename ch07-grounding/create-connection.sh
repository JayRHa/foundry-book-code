# Create a project-level Azure AI Search connection from a JSON definition
az cognitiveservices account project connection create \
  --name my-search-connection \
  --account-name my-foundry-resource \
  --project-name my-project \
  --resource-group rg-foundry \
  --file connection.json   # category: CognitiveSearch, authType: AAD
