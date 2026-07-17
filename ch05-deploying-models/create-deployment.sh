# Discover the exact model name, format, version, and supported SKUs
az cognitiveservices account list-models -n $accountName -g $rg

# Create the deployment (capacity 50 = 50k TPM for standard SKUs)
az cognitiveservices account deployment create -n $accountName -g $rg \
  --deployment-name gpt-4.1 --model-name gpt-4.1 --model-version 2025-04-14 \
  --model-format OpenAI --sku-capacity 50 --sku-name GlobalStandard

# Verify
az cognitiveservices account deployment show --deployment-name gpt-4.1 \
  -n $accountName -g $rg --query properties.provisioningState
