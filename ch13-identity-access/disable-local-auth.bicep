// Foundry resource with key-based (local) authentication disabled
resource foundry 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: 'foundry-contoso-prod'
  location: 'swedencentral'
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  properties: {
    allowProjectManagement: true
    customSubDomainName: 'foundry-contoso-prod'
    disableLocalAuth: true // API keys stop working; Entra ID only
  }
}
