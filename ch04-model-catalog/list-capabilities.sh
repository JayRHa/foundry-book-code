# Which models here support fine-tuning? (far fewer than people expect)
az cognitiveservices model list -l swedencentral \
  --query "[?model.finetuneCapabilities].{name:model.name, version:model.version, status:model.lifecycleStatus}" \
  -o table

# What is on its way out, and when does inference stop?
az cognitiveservices model list -l swedencentral \
  --query "[?model.lifecycleStatus=='Deprecating'].{name:model.name, version:model.version, retires:model.deprecation.inference}" \
  -o table
