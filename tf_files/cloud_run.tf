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
    }
  }
  lifecycle {
    ignore_changes = [
      launch_stage,
    ]
  }
}