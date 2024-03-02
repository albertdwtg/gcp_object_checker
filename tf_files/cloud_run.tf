resource "google_service_account" "sa-jobs-launcher" {
  account_id   = "sa-jobs-launcher"
  display_name = "Jobs launcher job service account"
}

resource "google_cloud_run_v2_service" "jobs" {
  for_each = local.jobs
  name     = each.key
  location = var.region
  template {
    timeout = each.value.timeout
    containers {
      image = "europe-west1-docker.pkg.dev/${var.project_id}/jobs-launcher/${each.key}:${var.images_tag}"
      ports {
        container_port = var.cloud_run_port
      }
      resources {
        limits = {
          cpu    = each.value.max_cpu_job
          memory = each.value.max_memory_job
        }
      }
    }
    service_account = google_service_account.sa-jobs-launcher.email
  }
}