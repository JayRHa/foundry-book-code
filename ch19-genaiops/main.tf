# The Foundry resource: a cognitive account of kind AIServices
resource "azurerm_cognitive_account" "ai_foundry" {
  name                       = "aifoundry-prod"
  location                   = var.location
  resource_group_name        = azurerm_resource_group.rg.name
  kind                       = "AIServices"
  sku_name                   = "S0"
  custom_subdomain_name      = "aifoundry-prod"
  project_management_enabled = true          # this is what makes it a Foundry resource
  identity { type = "SystemAssigned" }
}

# The project: azurerm supports this today, no azapi needed
resource "azurerm_cognitive_account_project" "device_support" {
  name                 = "device-support"
  cognitive_account_id = azurerm_cognitive_account.ai_foundry.id
  location             = var.location
  identity { type = "SystemAssigned" }
}
