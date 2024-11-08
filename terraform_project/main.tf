provider "aws" {
  region = "eu-central-1"  # Frankfurt region
}

variable "ec2_instance_type" {
  default = "t3.micro"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "main_vpc"
  }
}

# Subnet
resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "public_subnet"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main_igw"
  }
}

# Route Table
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "public_route_table"
  }
}

# Route Table Association
resource "aws_route_table_association" "public_assoc" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public_rt.id
}

# Security Group for EC2
resource "aws_security_group" "ec2_sg" {
  vpc_id = aws_vpc.main.id

  # Allow inbound SSH (port 22)
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow inbound HTTP (port 80)
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ec2_sg"
  }
}

# EC2 Instance
resource "aws_instance" "web" {
  ami                         = "ami-0084a47cc718c111a"  # Replace with an appropriate AMI
  instance_type               = var.ec2_instance_type
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.ec2_sg.id]
  associate_public_ip_address = true
  key_name                    = "django_terraform"  

  # User data script to install Docker
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
              curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
              sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
              sudo apt update -y
              sudo apt install -y docker-ce docker-ce-cli containerd.io
              sudo systemctl enable docker
              sudo systemctl start docker
              EOF

  tags = {
    Name = "docker_instance"
  }
}

# Output for EC2 instance's public IP and DNS
output "ec2_public_ip" {
  value       = aws_instance.web.public_ip
  description = "The public IP address of the EC2 instance"
}

output "ec2_public_dns" {
  value       = aws_instance.web.public_dns
  description = "The public DNS name of the EC2 instance"
}

