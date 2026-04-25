variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "Cloud_Native_aks"
}

variable "location" {
  description = "Azure region for deployment"
  type        = string
  default     = "eastus"
}

variable "acr_name" {
  description = "Azure Container Registry name (must be globally unique)"
  type        = string
  default     = "cloudNativeAcr"
}

variable "aks_name" {
  description = "AKS cluster name"
  type        = string
  default     = "cloud-native-cluster"
}

variable "gh_org" {
  description = "Org for the handout repo"
  type        = string
  default     = "SAIL-Classroom" # The org in which the repo is present
}

variable "gh_repo" {
  description = "Name of the github repo"
  type        = string
  default     = "cloud-native-handout-prithiraj-bhuyan" # Your repo
}
