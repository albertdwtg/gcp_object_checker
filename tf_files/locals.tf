locals {
  topics_paths = jsonencode({ for k, v in local.jobs : k => google_pubsub_topic.jobs_launcher_topics[k].id })
  jobs = {
    first-job = {
      max_cpu_job    = 1
      max_memory_job = "512Mi"
      timeout        = "15s"
      max_retries    = 2
      scheduler = {
        description      = "First job scheduler"
        cron             = "*/30 * * * *"
        time_zone        = "Europe/Paris"
        attempt_deadline = "60s"
        paused           = false
      }
    }
    second-job = {
      max_cpu_job    = 1
      max_memory_job = "512Mi"
      timeout        = "15s"
      max_retries    = 2
      scheduler = {
        description      = "Second job scheduler"
        cron             = "*/10 * * * *"
        time_zone        = "Europe/Dublin"
        attempt_deadline = "60s"
        paused           = true
      }
    }
  }

  schedulers = {
    first-scheduler = {
      description      = "First job scheduler"
      cron             = "*/30 * * * *"
      time_zone        = "Europe/Paris"
      attempt_deadline = "60s"
      paused           = false
      body = base64encode(jsonencode(file("../schedulers/payload_1.json")))
    }
    second-scheduler = {
      description      = "Second job scheduler"
      cron             = "*/10 * * * *"
      time_zone        = "Europe/Dublin"
      attempt_deadline = "60s"
      paused           = true
      body = base64encode(jsonencode(file("../schedulers/payload_2.json")))
    }
  }

  cloud_runs = {
    first-job = {
      max_cpu_job    = 1
      max_memory_job = "512Mi"
      timeout        = "15s"
      max_retries    = 2
    }
    second-job = {
      max_cpu_job    = 1
      max_memory_job = "512Mi"
      timeout        = "15s"
      max_retries    = 2
    }
  }
}
