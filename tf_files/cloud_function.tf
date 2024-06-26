resource "google_service_account" "sa-cloud-function" {
  account_id  = "sa-cf-jobs-launcher"
  description = "Service account used by jobs launcher cloud function"
}

resource "google_cloudfunctions_function" "jobs_launcher_cf" {
  name        = "jobs_launcher"
  description = "Jobs launcher cloud function"
  runtime     = "python312"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.jobs_launcher_bucket.name
  source_archive_object = google_storage_bucket_object.blob_cf_code.name
  trigger_http          = true
  timeout               = 60
  entry_point           = "run"
  service_account_email = google_service_account.sa-cloud-function.email
  environment_variables = {
    "TOPIC_PATHS" = local.topics_paths
  }
  ingress_settings = "ALLOW_INTERNAL_ONLY"
}
