resource "google_service_account" "sa-jobs-launcher" {
  account_id   = "sa-jobs-launcher"
  display_name = "Jobs launcher job service account"
}

# resource "google_cloud_run_v2_job" "object_checker" {
#   name     = var.project_id
#   location = var.region
#   template {
#     template {
#       containers {
#         image = "${var.artifact_registry_image_name}:latest"
#         resources {
#           limits = {
#             cpu    = var.max_cpu_job
#             memory = var.max_memory_job
#           }
#         }
#       }
#       service_account = google_service_account.sa-job-obj-checker.email
#     }
#   }
#   lifecycle {
#     ignore_changes = [
#       launch_stage,
#     ]
#   }
# }

resource "google_cloud_run_v2_job" "object_checker" {
  for_each = local.jobs
  name     = each.key
  location = var.region
  template {
    template {
      containers {
        # image = "europe-west1-docker.pkg.dev/${var.project_id}/jobs-launcher/${each.key}"
        image = "europe-west1-docker.pkg.dev/model-zoo-382809/jobs-launcher/first-job:551d297663f0914ed36141afd9ba55d589ab3021"
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
}