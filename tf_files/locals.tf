locals {
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
        body = {
          var1 = "Test1"
          var2 = "Test2"
        }
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
        body = {
          var1 = "Test1"
          var2 = "Test2"
        }
      }
    }
  }
}