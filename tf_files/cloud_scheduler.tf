resource "google_cloud_scheduler_job" "schedulers" {
  for_each         = local.jobs
  name             = each.key
  description      = each.value.scheduler.description
  schedule         = each.value.scheduler.cron
  time_zone        = lookup(each.value.scheduler, "time_zone", var.default_time_zone)
  attempt_deadline = lookup(each.value.scheduler, "attempt_deadline", var.default_attempt_deadline)
  paused           = lookup(each.value.scheduler, "paused", var.default_paused)

  http_target {
    http_method = "POST"
    uri         = google_cloudfunctions_function.jobs_launcher_cf.https_trigger_url
    body        = base64encode(jsonencode(file("../src/${each.key}/payload.json")))
    headers = {
      "Content-Type" = "application/json"
      "Body-Hash" = md5(file("../src/${each.key}/payload.json"))
    }
    oidc_token {
      service_account_email = google_service_account.sa-cloud-function.email
    }
  }
}