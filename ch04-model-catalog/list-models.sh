# Which OpenAI models can I deploy in this region, in which version, and in which lifecycle state?
az cognitiveservices model list -l swedencentral \
  --query "[?kind=='OpenAI'].{name:model.name, version:model.version, status:model.lifecycleStatus}" \
  -o table

# And which deployment SKUs does one specific model support here?
az cognitiveservices model list -l swedencentral \
  --query "[?model.name=='gpt-5.4'].model.skus[].name" -o tsv
