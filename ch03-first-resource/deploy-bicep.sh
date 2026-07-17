az group create --name exampleRG --location eastus
az deployment group create --resource-group exampleRG \
  --template-file main.bicep --parameters aiFoundryName=myai aiProjectName=myai-proj
