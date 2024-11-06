provider "aws" {
  region = "eu-central-1"
}


terraform {
  required_providers {
    github = {
      source  = "integrations/github"
      version = "6.3.1"
    }
  }
}
