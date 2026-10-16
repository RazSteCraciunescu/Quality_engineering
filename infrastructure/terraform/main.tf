terraform {
  required_version = ">= 1.7.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  type    = string
  default = "West Europe"
}

variable "image" {
  type    = string
  default = "ghcr.io/example/civicshift:1.0.0"
}

resource "azurerm_resource_group" "civicshift" {
  name     = "rg-civicshift-demo"
  location = var.location
}

resource "azurerm_log_analytics_workspace" "civicshift" {
  name                = "log-civicshift-demo"
  location            = azurerm_resource_group.civicshift.location
  resource_group_name = azurerm_resource_group.civicshift.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "civicshift" {
  name                       = "cae-civicshift-demo"
  location                   = azurerm_resource_group.civicshift.location
  resource_group_name        = azurerm_resource_group.civicshift.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.civicshift.id
}

resource "azurerm_container_app" "civicshift" {
  name                         = "civicshift-demo"
  container_app_environment_id = azurerm_container_app_environment.civicshift.id
  resource_group_name          = azurerm_resource_group.civicshift.name
  revision_mode                = "Single"

  template {
    min_replicas = 1
    max_replicas = 1

    container {
      name   = "app"
      image  = var.image
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "CIVICSHIFT_AI_PROVIDER"
        value = "rules"
      }

      env {
        name  = "CIVICSHIFT_DB"
        value = "/tmp/civicshift.db"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
