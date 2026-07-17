# Get an Entra token and create a prompt agent via REST
TOKEN=$(az account get-access-token --scope https://ai.azure.com/.default \
        --query accessToken -o tsv)

curl -X POST "$PROJECT_ENDPOINT/agents?api-version=v1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "MyAgent",
        "definition": {
          "kind": "prompt",
          "model": "gpt-5.4-mini",
          "instructions": "You are a helpful assistant that answers general questions"
        }
      }'
