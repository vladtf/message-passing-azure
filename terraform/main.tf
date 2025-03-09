provider "azurerm" {
  features {}
  subscription_id = "60344ef8-bcbb-43f9-9d2b-287fd7a054fd"
}

# Create a Resource Group
resource "azurerm_resource_group" "soam" {
  name     = "soam-rg"
  location = "East US"
}

# Create a Service Bus Namespace
resource "azurerm_servicebus_namespace" "soam" {
  name                = "soam-sb-namespace"
  location            = azurerm_resource_group.soam.location
  resource_group_name = azurerm_resource_group.soam.name
  sku                 = "Standard"
}

# Create a Service Bus Topic (acts like SNS)
resource "azurerm_servicebus_topic" "soam_topic" {
  name         = "soam-topic"
  namespace_id = azurerm_servicebus_namespace.soam.id

  # Optional: enable partitioning for better scalability
  partitioning_enabled = true
}

# Create a Service Bus Subscription (acts like an SQS queue subscribed to the SNS topic)
resource "azurerm_servicebus_subscription" "soam_subscription" {
  name     = "soam-subscription"
  topic_id = azurerm_servicebus_topic.soam_topic.id

  # Configure the maximum delivery attempts before sending the message to the dead-letter queue
  max_delivery_count = 10
}

# (Optional) Create an Authorization Rule for the Topic so your application can publish messages
resource "azurerm_servicebus_topic_authorization_rule" "soam_topic_auth" {
  name     = "soam-topic-auth"
  topic_id = azurerm_servicebus_topic.soam_topic.id

  listen = true
  send   = true
  manage = false
}
