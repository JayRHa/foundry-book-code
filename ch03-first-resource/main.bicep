// main.bicep — minimal Foundry resource with one project
param aiFoundryName string
param aiProjectName string
param location string = resourceGroup().location

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiFoundryName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    allowProjectManagement: true
    customSubDomainName: aiFoundryName
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: account
  name: aiProjectName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {}
}
