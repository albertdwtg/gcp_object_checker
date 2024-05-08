resource "google_cloud_scheduler_job" "schedulers" {
  for_each         = local.jobs
  name             = each.key
  description      = each.value.scheduler.description
  schedule         = each.value.scheduler.cron
  time_zone        = each.value.scheduler.time_zone
  attempt_deadline = each.value.scheduler.attempt_deadline
  paused           = each.value.scheduler.paused

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.jobs_launcher_cf.https_trigger_url
    # body        = base64encode(replace(jsonencode(each.value.scheduler.body), "\"", ""))
    body        = base64encode(replace(jsonencode(file("../src/${each.key}/payload.json"))), "\"", "")
    headers = {
      "Content-Type" = "application/json"
    }
    oidc_token {
      service_account_email = google_service_account.sa-cloud-function.email
    }
  }
}