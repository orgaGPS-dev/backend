variable "instance_type" {
  description = "The type of AWS instance to be created, e.g., t4g.nano for ARM instances"
  type        = string
  default     = "t4g.nano"
}

variable "ami_id" {
  description = "The Amazon Machine Image (AMI) ID for an ARM-compatible Ubuntu instance in eu-central-1"
  type        = string
  default     = "ami-099a546c02844706e"
}

