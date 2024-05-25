resource "google_bigquery_dataset_iam_member" "editor" {
  dataset_id = google_bigquery_dataset.raw_data_dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.cloud-run-sa-email}"
}

# resource "google_bigquery_dataset_iam_member" "user" {
#   dataset_id = google_bigquery_dataset.raw_data_dataset.dataset_id
#   role       = "roles/bigquery.user"
#   member     = "serviceAccount:${var.cloud-run-sa-email}"
# }

resource "google_project_iam_member" "bq_user" {
  project = var.project_id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${var.cloud-run-sa-email}"
}
