resource "google_service_account" "sa-job-obj-checker" {
  account_id   = "sa-obj-checker-job"
  display_name = "Object Checker Job service account"
}


resource "google_cloud_run_v2_job" "object_checker" {
  name     = var.project_id
  location = var.region
  template {
    template {
      containers {
        image = "${var.artifact_registry_image_name}:latest"
        resources {
          limits = {
            cpu    = var.max_cpu_job
            memory = var.max_memory_job
          }
        }
      }
      service_account = google_service_account.sa-job-obj-checker.email
    }
  }
  lifecycle {
    ignore_changes = [
      launch_stage,
    ]
  }
}