provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "sms-spam-classifier" {
  name     = "sms-spam-classifier-resource-group"
  location = "australiaeast"
}

resource "azurerm_container_group" "sms-spam-classifier" {
  name                = "sms-spam-classifier-container-group"
  location            = azurerm_resource_group.sms-spam-classifier.location
  resource_group_name = azurerm_resource_group.sms-spam-classifier.name

  os_type      = "Linux"
  dns_name_label = "sms-spam-classifier-dns-label"

  container {
    name   = "sms-spam-classifier-container"
    image  = "carlongo/sms-spam-classifier:v1.2"
    cpu    = "0.5"
    memory = "1.5"
    ports {
      port     = 80
      protocol = "TCP"
    }
  }
}