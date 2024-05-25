resource "google_bigquery_dataset_iam_member" "editor" {
  dataset_id = google_bigquery_dataset.raw_data_dataset.dataset_id
  role       = "roles/bigquery.dataEditor"
  member     = "serviceAccount:${var.cloud-run-sa-email}"
}