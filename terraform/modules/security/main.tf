variable "app_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "alb_sg_id" {
  type = string
}

# ECS Security Group
resource "aws_security_group" "ecs" {
  name        = "${var.app_name}-ecs-sg"
  vpc_id      = var.vpc_id

  # Allow inbound from ALB
  ingress {
    from_port       = 8000
    to_port         = 8000
    protocol        = "tcp"
    security_groups = [var.alb_sg_id]
  }

  # Allow all outbound (for MongoDB Atlas, Docker pulls, etc.)
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.app_name}-ecs-sg"
  }
}

# Outputs
output "ecs_sg_id" {
  value = aws_security_group.ecs.id
}
