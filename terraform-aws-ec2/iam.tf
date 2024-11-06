# Define the IAM role for EC2 access to S3
resource "aws_iam_role" "ec2_s3_access_role" {
  name = "orgagps-ec2-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_policy" "s3_access_policy" {
  name        = "orgagps-terraform-access-policy"
  description = "Policy for EC2 access to S3 bucket orgagps-terraform-state"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ],
        Resource = [
          "arn:aws:s3:::orgagps-terraform-state",
          "arn:aws:s3:::orgagps-terraform-state/*"
        ]
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Attach the S3 policy to the IAM role
resource "aws_iam_role_policy_attachment" "attach_s3_policy" {
  role       = aws_iam_role.ec2_s3_access_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn

  lifecycle {
    create_before_destroy = true
  }
}

# Create the IAM instance profile with the EC2 role
resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "orgagps_ec2_instance_profile"
  role = aws_iam_role.ec2_s3_access_role.name

  lifecycle {
    create_before_destroy = true
  }
}

# Define the IAM role for CodeBuild
resource "aws_iam_role" "codebuild_role" {
  name = "orgagps-codebuild-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "codebuild.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Custom policy for CodeBuild role
resource "aws_iam_policy" "custom_codebuild_policy" {
  name        = "orgagps-custom-codebuild-policy"
  description = "Custom policy to manage CodeBuild permissions"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "codebuild:StartBuild",
          "codebuild:BatchGetBuilds",
          "codebuild:StopBuild",
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
        ],
        Resource = [
          "arn:aws:s3:::orgagps-pipeline-artifacts",
          "arn:aws:s3:::orgagps-pipeline-artifacts/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = [
          "arn:aws:logs:eu-central-1:442426882318:log-group:/aws/codebuild/orgagps-frontend-project:*",
          "arn:aws:logs:eu-central-1:442426882318:log-group:/aws/codebuild/orgagps-backend-project:*"
        ]
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}


# Attach the custom CodeBuild policy to the CodeBuild role
resource "aws_iam_role_policy_attachment" "attach_custom_codebuild_policy" {
  role       = aws_iam_role.codebuild_role.name
  policy_arn = aws_iam_policy.custom_codebuild_policy.arn

  lifecycle {
    create_before_destroy = true
  }
}

# Define the IAM role for CodePipeline
resource "aws_iam_role" "codepipeline_role" {
  name = "orgagps-codepipeline-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "codepipeline.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Custom policy for CodePipeline role
resource "aws_iam_policy" "custom_codepipeline_policy" {
  name        = "orgagps-custom-codepipeline-policy"
  description = "Custom policy for CodePipeline access"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "codepipeline:*",       # Volle Berechtigungen für CodePipeline
          "s3:*",                 # Volle Berechtigungen für den Zugriff auf die S3-Buckets
          "codebuild:*" 
        ],
        Resource = [
          "arn:aws:s3:::orgagps-pipeline-artifacts",
          "arn:aws:s3:::orgagps-pipeline-artifacts/*",
          "arn:aws:codebuild:eu-central-1:442426882318:project/orgagps-frontend-project",  # Ersetze mit dem spezifischen CodeBuild-Projekt
          "arn:aws:codebuild:eu-central-1:442426882318:project/orgagps-backend-project",    # Ersetze mit dem spezifischen CodeBuild-Projekt
        ]
      }
    ]
  })
}

# Attach the custom CodePipeline policy to the CodePipeline role
resource "aws_iam_role_policy_attachment" "attach_custom_codepipeline_policy" {
  role       = aws_iam_role.codepipeline_role.name
  policy_arn = aws_iam_policy.custom_codepipeline_policy.arn

  lifecycle {
    create_before_destroy = true
  }
}

# Policy for access to Secrets Manager
resource "aws_iam_policy" "secrets_manager_access_policy" {
  name        = "orgagps-secrets-manager-access-policy"
  description = "Policy to allow access to AWS Secrets Manager"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ],
        Resource = "arn:aws:secretsmanager:eu-central-1:442426882318:secret:orgagps-app-secrets"
      }
    ]
  })

  lifecycle {
    create_before_destroy = true
  }
}

# Attach the Secrets Manager policy to the CodeBuild role
resource "aws_iam_role_policy_attachment" "attach_secrets_manager_policy" {
  role       = aws_iam_role.codebuild_role.name
  policy_arn = aws_iam_policy.secrets_manager_access_policy.arn

  lifecycle {
    create_before_destroy = true
  }
}

# Reference the existing Secrets Manager secret
data "aws_secretsmanager_secret" "app_secrets" {
  name = "orgagps-app-secrets"
}

