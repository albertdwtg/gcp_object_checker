variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "label_value" {
  type        = string
  description = "Label to use on resource for this project"
  default     = "air_quality"
}

variable "cloud-run-sa-email" {
  type        = string
  description = "Email of the service account used by cloud run"
}

variable "open_weather_api_secret" {
  type        = string
  description = "Secret api key to use in open weather api"
}
