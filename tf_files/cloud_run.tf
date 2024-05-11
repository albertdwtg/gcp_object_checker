resource "google_service_account" "sa-jobs-launcher" {
  account_id  = "sa-jobs-launcher"
  description = "Jobs launcher service account"
}

resource "google_cloud_run_v2_service" "jobs" {
  for_each    = local.jobs
  name        = each.key
  location    = var.region
  description = "Job ${each.key} deployed with Jobs Launcher"
  ingress     = "INGRESS_TRAFFIC_INTERNAL_ONLY"
  template {
    timeout = lookup(each.value, "timeout", var.default_timeout)
    containers {
      image = "europe-west1-docker.pkg.dev/${var.project_id}/jobs-launcher/${each.key}:${var.images_tag}"
      ports {
        container_port = var.cloud_run_port
      }
      resources {
        limits = {
          cpu    = lookup(each.value, "max_cpu_job", var.default_max_cpu)
          memory = lookup(each.value, "max_memory_job", var.default_max_memory)
        }
      }
      env {
        name  = "CONTAINER_PORT"
        value = var.cloud_run_port
      }
    }
    service_account = google_service_account.sa-jobs-launcher.email
  }
}
