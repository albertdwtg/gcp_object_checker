resource "google_pubsub_topic" "jobs_launcher_topics" {
  for_each = local.cloud_runs
  name     = "topic-launcher-${each.key}"
}

resource "google_pubsub_subscription" "jobs_launcher_subscription" {
  for_each                   = local.cloud_runs
  name                       = "subscription-launcher-${each.key}"
  topic                      = google_pubsub_topic.jobs_launcher_topics[each.key].name
  retain_acked_messages      = false
  message_retention_duration = "600s"
  ack_deadline_seconds       = 600

  push_config {
    push_endpoint = google_cloud_run_v2_service.jobs[each.key].uri
    oidc_token {
      service_account_email = google_service_account.sa-jobs-launcher.email
    }
    attributes = {
      x-goog-version = "v1"
    }
  }
  expiration_policy {
    ttl = ""
  }
  retry_policy {
    minimum_backoff = "600s"
  }
  depends_on = [google_cloud_run_v2_service.jobs]
}
