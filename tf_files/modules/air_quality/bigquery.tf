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

  time_partitioning {
    type  = "DAY"
    field = "utc_timestamp"
  }
  schema = <<EOF
    [
    {
        "name": "utc_timestamp",
        "type": "TIMESTAMP",
        "mode": "NULLABLE"
    },
    {
        "name": "latitude",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "longitude",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "air_quality_index",
        "type": "INT64",
        "mode": "NULLABLE"
    },
    {
        "name": "co",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "no",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "no2",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "o3",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "so2",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "pm2_5",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "pm10",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    },
    {
        "name": "nh3",
        "type": "FLOAT64",
        "mode": "NULLABLE"
    }
    ]
    EOF
  labels = {
    env = var.label_value
  }
}
