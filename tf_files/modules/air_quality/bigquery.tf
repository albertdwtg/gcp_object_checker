resource "google_bigquery_dataset" "raw_data_dataset" {
  project     = var.project_id
  dataset_id  = "raw_data_air_quality"
  description = "Dataset that contains all raw data of air quality project"
  location    = "europe-west9"
  labels = {
    project = var.label_value
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.raw_data_dataset.dataset_id
  table_id   = "test"

#   time_partitioning {
#     type  = "DAY"
#     field = "utc_datetime"
#   }

  labels = {
    env = var.label_value
  }
}
