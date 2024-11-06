terraform {
  backend "s3" {
    bucket         = "orgagps-terraform-state"  # Der Name des Buckets als statischer Wert
    key            = "state/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
  }
}
