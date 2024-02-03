resource "google_cloud_run_v2_job" "object_checker" {
  name     = "object_checker_job"
  location = "us-central1"

  template {
    template {
      containers {
        image = "us-docker.pkg.dev/cloudrun/container/hello"
        resources {
          limits = {
            cpu    = "2"
            memory = "1024Mi"
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