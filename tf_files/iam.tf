# resource "google_project_iam_custom_role" "impersonification_role" {
#   role_id     = "impersonification_role"
#   title       = "Impersonification Role"
#   description = "Role to impersonate Service account"
#   permissions = ["iam.serviceaccounts.actAs"]
# }

# resource "google_cloud_run_service_iam_member" "invoker_jobs" {
#   for_each = local.jobs
#   service  = google_cloud_run_v2_service.jobs[each.key].name
#   role     = "roles/run.invoker"
#   member   = "serviceAccount:${google_service_account.sa-cloud-function.email}"
# }

resource "google_cloud_run_service_iam_member" "invoker_jobs" {
  for_each = local.jobs
  service  = google_cloud_run_v2_service.jobs[each.key].name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.sa-jobs-launcher.email}"
}

resource "google_cloudfunctions_function_iam_member" "invoker_cf" {
  project        = google_cloudfunctions_function.jobs_launcher_cf.project
  region         = google_cloudfunctions_function.jobs_launcher_cf.region
  cloud_function = google_cloudfunctions_function.jobs_launcher_cf.name

  role   = "roles/cloudfunctions.invoker"
  member = "serviceAccount:${google_service_account.sa-cloud-function.email}"
}

# resource "google_pubsub_subscription_iam_member" "subscription_editor" {
#   for_each     = local.jobs
#   subscription = google_pubsub_subscription.jobs_launcher_subscription[each.key].name
#   role         = "roles/editor"
#   member       = "serviceAccount:${google_service_account.sa-cloud-function.email}"
# }

resource "google_pubsub_topic_iam_member" "topic_editor" {
  for_each = local.jobs
  project  = google_pubsub_topic.jobs_launcher_topics[each.key].project
  topic    = google_pubsub_topic.jobs_launcher_topics[each.key].name
  role     = "roles/editor"
  member   = "serviceAccount:${google_service_account.sa-cloud-function.email}"
}
