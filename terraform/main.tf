provider "azurerm" {
  features {}
  subscription_id = "01810409-8e44-41af-a73f-b47942986098"
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

# Create a Service Bus Queue to which messages will be forwarded
resource "azurerm_servicebus_queue" "soam_queue" {
  name                = "soam-queue"
  namespace_id = azurerm_servicebus_namespace.soam.id
  # (Optional) specify additional queue settings as needed
}

# Create a Service Bus Subscription that forwards messages to the queue
resource "azurerm_servicebus_subscription" "soam_subscription" {
  name     = "soam-subscription"
  topic_id = azurerm_servicebus_topic.soam_topic.id

  # Configure the maximum delivery attempts before sending the message to the dead-letter queue
  max_delivery_count = 10

  # Forward incoming messages to the queue
  forward_to = azurerm_servicebus_queue.soam_queue.name
}

# (Optional) Create an Authorization Rule for the Topic so your application can publish messages
resource "azurerm_servicebus_topic_authorization_rule" "soam_topic_auth" {
  name     = "soam-topic-auth"
  topic_id = azurerm_servicebus_topic.soam_topic.id

  listen = true
  send   = true
  manage = false
}
