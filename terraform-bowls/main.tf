terraform {
  required_version = ">= 1.5.0"
}

resource "terraform_data" "bowls" {
  input = {
    project       = "Bowls"
    environment   = "local"
    container     = "Docker"
    orchestration = "Kubernetes"
  }
}