# Get an Entra token and call the Responses API on the project endpoint
TOKEN=$(az account get-access-token \
  --scope https://ai.azure.com/.default \
  --query accessToken -o tsv)

curl -X POST \
  "https://my-foundry-resource.services.ai.azure.com/api/projects/my-foundry-project/openai/v1/responses" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5.1-mini",
    "input": "Explain Intune error 0x87D00668 in one short paragraph."
  }'
