variable "app_name" {
  type = string
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "ecs" {
  name              = "/ecs/${var.app_name}"
  retention_in_days = 30

  tags = {
    Name = "${var.app_name}-logs"
  }
}

# CloudWatch Log Stream
resource "aws_cloudwatch_log_stream" "ecs" {
  name           = "api"
  log_group_name = aws_cloudwatch_log_group.ecs.name
}

# Outputs
output "log_group_name" {
  value = aws_cloudwatch_log_group.ecs.name
}

output "log_group_arn" {
  value = aws_cloudwatch_log_group.ecs.arn
}
