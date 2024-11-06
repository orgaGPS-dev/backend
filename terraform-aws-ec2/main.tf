
# Starten der EC2-Instanz und Zuweisen der Rolle
resource "aws_instance" "orgagps" {
  ami           = var.ami_id  # Beispiel-AMI-ID
  instance_type = var.instance_type
  subnet_id     = aws_subnet.main_subnet.id
  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  user_data = <<-EOF
    #!/bin/bash
    sudo apt-get update -y
    sudo apt-get install -y docker.io docker-compose git

    # Frontend und Backend klonen
    git clone https://github.com/orgaGPS/frontend.git /app/frontend
    git clone https://github.com/orgaGPS/backend.git /app/backend

    # Backend starten
    cd /app/backend
    docker-compose up -d

    # Frontend starten
    cd /app/frontend
    docker-compose up -d
  EOF

  tags = {
    Name = "orgagps"
  }
}

