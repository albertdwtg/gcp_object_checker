variable "region" {
  type = string
  description = "Region of project ressources"
}

variable "project_id" {
  type = string
  description = "GCP Project ID"
}

variable "artifact_registry_image_name"{
    type = string
    description = "Complete artifact registry image name for cloud run job"
}