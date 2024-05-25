terraform {
  backend "gcs" {
    bucket = "tf_state_object_checker"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "air_quality" {
  source                  = "./modules/air_quality"
  project_id              = var.project_id
  cloud-run-sa-email      = google_service_account.sa-jobs-launcher.email
  open_weather_api_secret = var.open_weather_api_secret
}
