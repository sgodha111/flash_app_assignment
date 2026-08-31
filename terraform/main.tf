terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Uncomment to use S3 backend
  # backend "s3" {
  #   bucket         = "antonie-books-terraform-state"
  #   key            = "prod/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-locks"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = var.tags
  }
}

# Data source for current AWS account
data "aws_caller_identity" "current" {}

data "aws_availability_zones" "available" {
  state = "available"
}

# VPC and Networking
module "networking" {
  source = "./modules/networking"

  app_name = var.app_name
  vpc_cidr = var.vpc_cidr
  az_count = length(data.aws_availability_zones.available.names)
  azs      = slice(data.aws_availability_zones.available.names, 0, 2)
}

# Security Groups
module "security" {
  source = "./modules/security"

  app_name   = var.app_name
  vpc_id     = module.networking.vpc_id
  vpc_cidr   = var.vpc_cidr
  alb_sg_id  = module.networking.alb_sg_id
}

# Application Load Balancer
module "alb" {
  source = "./modules/alb"

  app_name           = var.app_name
  vpc_id             = module.networking.vpc_id
  subnet_ids         = module.networking.public_subnet_ids
  security_group_id  = module.networking.alb_sg_id
  container_port     = var.container_port
}

# ECR Repository
module "ecr" {
  source = "./modules/ecr"

  app_name = var.app_name
}

# ECS Cluster, Task Definition, and Service
module "ecs" {
  source = "./modules/ecs"

  app_name              = var.app_name
  environment           = var.environment
  container_port        = var.container_port
  container_image       = var.container_image
  task_cpu              = var.task_cpu
  task_memory           = var.task_memory
  desired_count         = var.desired_count
  alb_target_group_arn  = module.alb.target_group_arn
  ecs_security_group_id = module.security.ecs_sg_id
  subnet_ids            = module.networking.private_subnet_ids
  mongodb_atlas_uri     = var.mongodb_atlas_uri
  database_name         = var.database_name
  cloudwatch_log_group  = module.logging.log_group_name
  task_execution_role   = module.iam.ecs_task_execution_role_arn
  task_role             = module.iam.ecs_task_role_arn
}

# IAM Roles and Policies
module "iam" {
  source = "./modules/iam"

  app_name = var.app_name
}

# CloudWatch Logging
module "logging" {
  source = "./modules/logging"

  app_name = var.app_name
}

# Outputs
output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.alb.alb_dns_name
}

output "ecr_repository_url" {
  description = "ECR repository URL for pushing images"
  value       = module.ecr.repository_url
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = module.ecs.cluster_name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = module.ecs.service_name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for ECS tasks"
  value       = module.logging.log_group_name
}
