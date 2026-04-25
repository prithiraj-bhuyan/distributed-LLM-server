terraform {
  required_version = ">= 1.6.0"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    github = {
    source  = "integrations/github"
    version = "6.9.0"
  }
  }
}

provider "azurerm" {
  features {}
}

provider "github" {
  owner = var.gh_org
}

# ------------------------
# Resource Group
# ------------------------
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group
resource "azurerm_resource_group" "rg" {
  # TODO 1: resource group name
  # There's a resource_group_name variable declared in the variables.tf file. Do NOT hard code the 
  # resource group name below. Instead, make a reference to the variable name declared in the variables.tf file. 
  name     = var.resource_group_name

  # TODO 2: location
  # Reference the location name specified in the variables.tf file
  location = var.location
}

# ------------------------
# Azure Container Registry
# ------------------------
# Create Azure Container Registry
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/container_registry
resource "azurerm_container_registry" "acr" {
  # TODO 3: Container Registry Name
  # Reference the container registry name in the variables.tf file
  name                = var.acr_name

  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Standard"
  admin_enabled       = true
}


# ------------------------
# Azure Kubernetes Service (AKS)
# ------------------------
# https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/kubernetes_cluster
resource "azurerm_kubernetes_cluster" "aks" {
  # TODO 4: AKS Name
  # Reference the AKS name in the variables.tf file
  name                = var.aks_name

  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "bigklus"

  default_node_pool {
    name       = "default"
    node_count = 2

    # TODO 5: VM Size
    # You are to use the vm_size in the D-Series family with the following specifications:
    # - RAM: 8Gb
    # - vCPUs: 2
    # You can use the following command which outputs in tabular format, the various VM
    # sizes:
    #   az vm list-sizes --location eastus \
    #   --query "[?starts_with(name, 'Standard_D')]" \
    #   -o table
    # All you have to do is copy and paste the name of the vm size into the placeholder below:
    
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Production"
  }
}

# ------------------------
# Grant AKS access to ACR
# ------------------------
resource "azurerm_role_assignment" "ra" {
 principal_id                     = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
 role_definition_name             = "AcrPull"
 scope                            = azurerm_container_registry.acr.id
 skip_service_principal_aad_check = true
}

# ------------------------
# Outputs
# ------------------------
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}

output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "aks_kube_config" {
  value     = azurerm_kubernetes_cluster.aks.kube_config_raw
  sensitive = true
}

resource "github_actions_secret" "cr_secret" {
  repository = var.gh_repo
  secret_name       = "ACR_TOKEN"
  plaintext_value = azurerm_container_registry.acr.admin_password
}