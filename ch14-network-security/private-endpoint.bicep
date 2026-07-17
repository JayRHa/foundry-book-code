// Private endpoint for a Foundry account, target subresource "account"
resource foundryPe 'Microsoft.Network/privateEndpoints@2024-05-01' = {
  name: 'pe-foundry-prod'
  location: location
  properties: {
    subnet: { id: peSubnetId }
    privateLinkServiceConnections: [
      {
        name: 'foundry-account'
        properties: {
          privateLinkServiceId: foundryAccountId // Microsoft.CognitiveServices/accounts resource ID
          groupIds: [ 'account' ]
        }
      }
    ]
  }
}
