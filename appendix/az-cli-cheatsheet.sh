# Sign in and create a resource group
az login
az group create --name my-foundry-rg --location eastus

# Foundry resource (enable project management for a new resource)
az cognitiveservices account create \
    --name my-foundry-resource \
    --resource-group my-foundry-rg \
    --kind AIServices \
    --sku S0 \
    --location eastus \
    --custom-domain my-foundry-resource \
    --allow-project-management

# Project (child resource)
az cognitiveservices account project create \
    --name my-foundry-resource \
    --resource-group my-foundry-rg \
    --project-name my-foundry-project \
    --location eastus

# Verify provisioning state
az cognitiveservices account show -n my-foundry-resource -g my-foundry-rg \
  --query properties.provisioningState -o tsv

# Discover deployable models (name, format, version, SKU)
az cognitiveservices account list-models -n my-foundry-resource -g my-foundry-rg

# Model deployment
az cognitiveservices account deployment create \
    --name my-foundry-resource --resource-group my-foundry-rg \
    --deployment-name gpt-4.1 --model-name gpt-4.1 \
    --model-version "2025-04-14" --model-format OpenAI \
    --sku-capacity 50 --sku-name GlobalStandard

# Grant developer access (Foundry User role, by GUID)
PROJECT_ID=$(az cognitiveservices account project show -n my-foundry-resource \
  -g my-foundry-rg --project-name my-foundry-project --query id -o tsv)
az role assignment create --role "53ca6127-db72-4b80-b1b0-d745d6d5456d" \
  --assignee "user@contoso.com" --scope $PROJECT_ID
