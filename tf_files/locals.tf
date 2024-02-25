locals {
    jobs = {
        first-job = {
            max_cpu_job = 1
            max_memory_job = "512Mi"
            timeout = "15s"
            max_retries = 2
        }
        second-job = {
            max_cpu_job = 1
            max_memory_job = "512Mi"
            timeout = "15s"
            max_retries = 2
        }
    }
}