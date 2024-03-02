resource "google_storage_bucket" "jobs_launcher_bucket" {
  name     = "jobs_launcher_bucket"
  location = "EU"
}
data "archive_file" "zip_cf_code" {
  type        = "zip"
  output_path = "/tmp/function-source.zip"
  source_dir  = "../cloud_function_code/"
}
resource "google_storage_bucket_object" "blob_cf_code" {
  name   = "function_source.zip"
  bucket = google_storage_bucket.jobs_launcher_bucket.name
  source = data.archive_file.zip_cf_code.output_path 
}