locals {
  topics_paths = jsonencode({ for k, v in local.cloud_runs : k => google_pubsub_topic.jobs_launcher_topics[k].id })

  schedulers = {
    first-scheduler = {
      description      = "Job scheduler for daily data of open weather API for pollution"
      cron             = "* 2 * * *"
      time_zone        = "Europe/Paris"
      attempt_deadline = "60s"
      paused           = false
      body             = base64encode(jsonencode(file("../scheduler_payloads/payload_1.json")))
    }
    second-scheduler = {
      description      = "Second job scheduler"
      cron             = "*/10 * * * *"
      time_zone        = "Europe/Dublin"
      attempt_deadline = "60s"
      paused           = true
      body             = base64encode(jsonencode(file("../scheduler_payloads/payload_2.json")))
    }
  }

  cloud_runs = {
    first-job = {
      max_cpu_job                      = 1
      max_memory_job                   = "512Mi"
      timeout                          = "15s"
      max_retries                      = 2
      max_instance_count               = 1
      min_instance_count               = 0
      max_instance_request_concurrency = 80
    }
    second-job = {
      max_cpu_job                      = 1
      max_memory_job                   = "512Mi"
      timeout                          = "15s"
      max_retries                      = 2
      max_instance_count               = 1
      min_instance_count               = 0
      max_instance_request_concurrency = 80
    }
  }
}
