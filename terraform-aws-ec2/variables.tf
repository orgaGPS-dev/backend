variable "instance_type" {
  description = "The type of AWS instance to be created, e.g., t4g.nano for ARM instances"
  type        = string
  default     = "t2.micro"
}

variable "ami_id" {
  description = "The Amazon Machine Image (AMI) ID for an ARM-compatible Ubuntu instance in eu-central-1"
  type        = string
  default     = "ami-0745b7d4092315796"
}

