resource "google_secret_manager_secret" "open_weather_api_secret" {
  secret_id = "open_weather_api_secret"
  labels = {
    label = var.label_value
  }
  replication {
    auto {}
  }
}


resource "google_secret_manager_secret_version" "open_weather_key_version" {
  secret = google_secret_manager_secret.open_weather_api_secret.id
  secret_data = var.open_weather_api_secret
}
