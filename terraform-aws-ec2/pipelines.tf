# Retrieve GitHub token from AWS Secrets Manager
data "aws_secretsmanager_secret_version" "app_secrets_version" {
  secret_id = "orgagps-app-secrets"  # Ensure this is the correct secret name in Secrets Manager
}

locals {
  github_secrets = jsondecode(data.aws_secretsmanager_secret_version.app_secrets_version.secret_string)
}

# Reference the existing pipeline artifacts S3 bucket
data "aws_s3_bucket" "pipeline_artifacts" {
  bucket = "orgagps-pipeline-artifacts"  # Must match the bucket name created in deploy.sh
}

# Frontend CodePipeline using GitHub as Source
resource "aws_codepipeline" "frontend_pipeline" {
  name     = "orgagps-frontend-pipeline"
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = data.aws_s3_bucket.pipeline_artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["SourceArtifact"]

      configuration = {
        Owner      = "orgaGPS-dev"                    # Replace with your GitHub username or organization
        Repo       = "frontend"                           # Replace with the frontend repository name
        Branch     = "main"                                    # Specify the branch to use
        OAuthToken = local.github_secrets.github_client_secret # Corrected attribute name
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["SourceArtifact"]
      output_artifacts = ["BuildArtifact"]

      configuration = {
        ProjectName = aws_codebuild_project.frontend_project.name
      }
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Backend CodePipeline using GitHub as Source
resource "aws_codepipeline" "backend_pipeline" {
  name     = "orgagps-backend-pipeline"
  role_arn = aws_iam_role.codepipeline_role.arn

  artifact_store {
    location = data.aws_s3_bucket.pipeline_artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"

    action {
      name             = "Source"
      category         = "Source"
      owner            = "ThirdParty"
      provider         = "GitHub"
      version          = "1"
      output_artifacts = ["SourceArtifact"]

      configuration = {
        Owner      = "orgaGPS-dev"                    # Replace with your GitHub username or organization
        Repo       = "backend"                            # Replace with the backend repository name
        Branch     = "main"                                    # Specify the branch to use
        OAuthToken = local.github_secrets.github_client_secret # Corrected attribute name
      }
    }
  }

  stage {
    name = "Build"

    action {
      name             = "Build"
      category         = "Build"
      owner            = "AWS"
      provider         = "CodeBuild"
      version          = "1"
      input_artifacts  = ["SourceArtifact"]
      output_artifacts = ["BuildArtifact"]

      configuration = {
        ProjectName = aws_codebuild_project.backend_project.name
      }
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Frontend CodeBuild Project
resource "aws_codebuild_project" "frontend_project" {
  name          = "orgagps-frontend-project"
  service_role  = aws_iam_role.codebuild_role.arn
  build_timeout = 30

  source {
    type      = "CODEPIPELINE"
    buildspec = "buildspec.yml"  # Ensure you have a buildspec.yml in the GitHub repo
  }

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:5.0"
    type         = "LINUX_CONTAINER"
    environment_variable {
      name  = "GITHUB_TOKEN"
      value = local.github_secrets.github_client_secret  # Corrected attribute name
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Backend CodeBuild Project
resource "aws_codebuild_project" "backend_project" {
  name          = "orgagps-backend-project"
  service_role  = aws_iam_role.codebuild_role.arn
  build_timeout = 30

  source {
    type      = "CODEPIPELINE"
    buildspec = "buildspec.yml"  # Ensure you have a buildspec.yml in the GitHub repo
  }

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:5.0"
    type         = "LINUX_CONTAINER"
    environment_variable {
      name  = "GITHUB_TOKEN"
      value = local.github_secrets.github_client_secret  # Corrected attribute name
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}





