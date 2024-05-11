resource "google_cloud_scheduler_job" "schedulers" {
  for_each         = local.schedulers
  name             = each.key
  description      = each.value.description
  schedule         = each.value.cron
  time_zone        = each.value.time_zone
  attempt_deadline = each.value.attempt_deadline
  paused           = each.value.paused

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.jobs_launcher_cf.https_trigger_url
    body        = each.value.body
    headers = {
      "Content-Type" = "application/json"
      # "Body-Hash" = md5(file("../src/${each.key}/payload.json"))
    }
    oidc_token {
      service_account_email = google_service_account.sa-cloud-function.email
    }
  }
}