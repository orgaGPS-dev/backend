# VPC Definition
resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "main_vpc"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Subnetz Definition
resource "aws_subnet" "main_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-central-1a"  # Wählen Sie eine AZ in Ihrer Region
  tags = {
    Name = "main_subnet"
  }

  lifecycle {
    create_before_destroy = true
  }
}
