// Model deployment as a child of the Foundry resource (account)
resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2024-04-01-preview' = {
  parent: foundryAccount
  name: 'gpt-4.1'
  sku: {
    name: 'GlobalStandard'
    capacity: 50
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: 'gpt-4.1'
      version: '2025-04-14'
    }
    raiPolicyName: 'Microsoft.DefaultV2' // content filter policy
  }
}
