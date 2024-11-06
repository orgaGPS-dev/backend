#!/bin/bash

# Stop script on errors
set -e

# Install Terraform
if ! command -v terraform &> /dev/null; then
  echo "Installing Terraform..."
  curl -Lo /tmp/terraform.zip https://releases.hashicorp.com/terraform/1.3.0/terraform_1.3.0_linux_amd64.zip
  unzip -o /tmp/terraform.zip -d /usr/local/bin/
fi

# Set AWS region and bucket name
AWS_REGION="eu-central-1"
S3_BUCKET_NAME="orgagps-terraform-state"
PIPELINE_BUCKET_NAME="orgagps-pipeline-artifacts"

# Check if the S3 bucket exists
if aws s3api head-bucket --bucket "$S3_BUCKET_NAME" --region "$AWS_REGION" 2>/dev/null; then
  echo "S3 bucket $S3_BUCKET_NAME already exists."
else
  echo "Creating S3 bucket: $S3_BUCKET_NAME"
  aws s3api create-bucket --bucket "$S3_BUCKET_NAME" --region "$AWS_REGION" \
    --create-bucket-configuration LocationConstraint="$AWS_REGION"
fi

# Enable versioning on the S3 bucket if it's not already enabled
CURRENT_VERSIONING_STATUS=$(aws s3api get-bucket-versioning --bucket "$S3_BUCKET_NAME" --query 'Status' --output text)
if [[ "$CURRENT_VERSIONING_STATUS" != "Enabled" ]]; then
  echo "Enabling versioning on the S3 bucket $S3_BUCKET_NAME..."
  aws s3api put-bucket-versioning --bucket "$S3_BUCKET_NAME" --versioning-configuration Status=Enabled
else
  echo "Versioning is already enabled on the S3 bucket $S3_BUCKET_NAME."
fi

# Check if the pipeline artifacts S3 bucket exists
if aws s3api head-bucket --bucket "$PIPELINE_BUCKET_NAME" --region "$AWS_REGION" 2>/dev/null; then
  echo "Pipeline artifacts S3 bucket $PIPELINE_BUCKET_NAME already exists."
else
  echo "Creating S3 bucket for pipeline artifacts: $PIPELINE_BUCKET_NAME"
  aws s3api create-bucket --bucket "$PIPELINE_BUCKET_NAME" --region "$AWS_REGION" \
    --create-bucket-configuration LocationConstraint="$AWS_REGION"
fi

# Enable versioning on the pipeline artifacts S3 bucket if not already enabled
CURRENT_PIPELINE_VERSIONING_STATUS=$(aws s3api get-bucket-versioning --bucket "$PIPELINE_BUCKET_NAME" --query 'Status' --output text)
if [[ "$CURRENT_PIPELINE_VERSIONING_STATUS" != "Enabled" ]]; then
  echo "Enabling versioning on pipeline artifacts S3 bucket $PIPELINE_BUCKET_NAME..."
  aws s3api put-bucket-versioning --bucket "$PIPELINE_BUCKET_NAME" --versioning-configuration Status=Enabled
else
  echo "Versioning is already enabled on pipeline artifacts S3 bucket $PIPELINE_BUCKET_NAME."
fi

# Initialize Terraform
terraform init

# Create a Terraform plan
echo "Creating Terraform plan..."
terraform plan

# Apply the Terraform configuration
echo "Applying Terraform configuration..."
terraform apply -auto-approve

echo "Deployment completed."
