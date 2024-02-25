# resource "google_project_iam_custom_role" "impersonification_role" {
#   role_id     = "impersonification_role"
#   title       = "Impersonification Role"
#   description = "Role to impersonate Service account"
#   permissions = ["iam.serviceaccounts.actAs"]
# }