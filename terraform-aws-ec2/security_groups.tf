# Sicherheitsgruppe für ECS
resource "aws_security_group" "ecs_sg" {
  name        = "allow_web_traffic"
  description = "Allow web inbound traffic"
  vpc_id      = aws_vpc.main_vpc.id  # Referenziert die VPC aus network.tf

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ecs_sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}
