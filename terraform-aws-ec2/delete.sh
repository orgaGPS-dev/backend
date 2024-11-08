#!/bin/bash

# Stop script on errors
set -e

# Load AWS Credentials from Secrets Manager
export AWS_REGION="eu-central-1"
SECRET_NAME="orgagps-app-secrets"

ACCESS_KEYS_JSON=$(aws secretsmanager get-secret-value --secret-id $SECRET_NAME --query SecretString --output text --region $AWS_REGION)
export AWS_ACCESS_KEY_ID=$(echo $ACCESS_KEYS_JSON | jq -r '.AWS_ACCESS_KEY_ID')
export AWS_SECRET_ACCESS_KEY=$(echo $ACCESS_KEYS_JSON | jq -r '.AWS_SECRET_ACCESS_KEY')

# Delete Terraform-managed resources
echo "Destroying all Terraform-managed resources..."
terraform init -backend-config="bucket=orgagps-terraform-state" -reconfigure
terraform destroy -auto-approve

# Empty and delete S3 buckets manually since Terraform destroy doesn't delete non-empty buckets
S3_BUCKETS=("orgagps-terraform-state" "orgagps-pipeline-artifacts")
for bucket in "${S3_BUCKETS[@]}"; do
  echo "Emptying and deleting S3 bucket: $bucket"
  aws s3 rm s3://$bucket --recursive --region $AWS_REGION
  aws s3api delete-bucket --bucket $bucket --region $AWS_REGION
done

# Detach and delete IAM policies and roles manually if not managed by Terraform
IAM_ROLES=("orgagps-ec2-role" "orgagps-codebuild-role" "orgagps-codepipeline-role")
IAM_POLICIES=("orgagps-terraform-access-policy" "orgagps-custom-codebuild-policy" "orgagps-custom-codepipeline-policy" "orgagps-secrets-manager-access-policy")

for policy in "${IAM_POLICIES[@]}"; do
  echo "Deleting IAM policy: $policy"
  POLICY_ARN=$(aws iam list-policies --query "Policies[?PolicyName=='$policy'].Arn" --output text)
  if [ -n "$POLICY_ARN" ]; then
    aws iam delete-policy --policy-arn "$POLICY_ARN"
  fi
done

for role in "${IAM_ROLES[@]}"; do
  echo "Detaching and deleting IAM role: $role"
  ATTACHED_POLICIES=$(aws iam list-attached-role-policies --role-name "$role" --query 'AttachedPolicies[*].PolicyArn' --output text)
  for policy_arn in $ATTACHED_POLICIES; do
    aws iam detach-role-policy --role-name "$role" --policy-arn "$policy_arn"
  done
  aws iam delete-role --role-name "$role"
done

# Confirm deletion
echo "All resources deleted successfully."
