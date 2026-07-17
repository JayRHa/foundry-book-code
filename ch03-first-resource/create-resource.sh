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

# Verify
az cognitiveservices account show -n my-foundry-resource -g my-foundry-rg \
  --query properties.provisioningState -o tsv
az cognitiveservices account project show -n my-foundry-resource -g my-foundry-rg \
  --project-name my-foundry-project --query properties.provisioningState -o tsv
