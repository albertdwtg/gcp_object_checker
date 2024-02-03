terraform {
  backend "gcs" {
    bucket = "tf_state_object_checker"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}