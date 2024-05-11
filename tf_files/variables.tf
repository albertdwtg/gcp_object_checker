variable "region" {
  type        = string
  description = "Region of project ressources"
}

variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "artifact_registry_image_name" {
  type        = string
  description = "Complete artifact registry image name for cloud run job"
}

variable "max_cpu_job" {
  type        = string
  description = "Max CPU to use for cloud run job"
  default     = "2"
}

variable "max_memory_job" {
  type        = string
  description = "Max memory to use for cloud run job"
  default     = "512Mi"
}

variable "images_tag" {
  type        = string
  description = "Tag of the images, based on commit tag"
}

variable "cloud_run_port" {
  type        = number
  description = "Port on which cloud run will listen"
}

#### DEFAULT VARIABLES ####

variable "default_paused" {
  type        = bool
  description = "Default value used for paused param in scheduler"
}

variable "default_time_zone" {
  type        = string
  description = "Default value used for time_zone param in scheduler"
}

variable "default_attempt_deadline" {
  type        = string
  description = "Default value used for attempt_deadline param in scheduler"
}

variable "default_max_cpu" {
  type        = number
  description = "Default value used for cpu param in cloud run"
}

variable "default_max_memory" {
  type        = string
  description = "Default value used for memory param in cloud run"
}

variable "default_timeout" {
  type        = string
  description = "Default value used for timeout param in cloud run"
}