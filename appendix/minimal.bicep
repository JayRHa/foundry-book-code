param aiFoundryName string = 'foundry-name'
param aiProjectName string = '${aiFoundryName}-proj'
param location string = 'eastus2'

// A Foundry resource is a variant of a CognitiveServices/account resource type
resource aiFoundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: aiFoundryName
  location: location
  identity: { type: 'SystemAssigned' }
  sku: { name: 'S0' }
  kind: 'AIServices'
  properties: {
    allowProjectManagement: true   // required to work in Foundry
    customSubDomainName: aiFoundryName
    disableLocalAuth: false
  }
}

// Projects group developer APIs, files, agents for one use case
resource aiProject 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  name: aiProjectName
  parent: aiFoundry
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {}
}

// Model deployment (playground, agents, tools)
resource modelDeployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: aiFoundry
  name: 'gpt-4.1-mini'
  sku: { capacity: 1, name: 'GlobalStandard' }
  properties: {
    model: { name: 'gpt-4.1-mini', format: 'OpenAI', version: '2025-04-14' }
  }
}
