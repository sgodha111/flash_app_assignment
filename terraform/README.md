# Antonie Book Catalog - AWS Infrastructure (Terraform)

This directory contains Terraform infrastructure-as-code for deploying the Antonie Book Catalog API to AWS.

## Architecture Overview

```
Internet
    |
    v
Application Load Balancer (ALB)
    |
    v
AWS Fargate (ECS)
    |
    v
FastAPI Application Container
    |
    v
MongoDB Atlas
```

## Prerequisites

- Terraform >= 1.0
- AWS CLI configured with credentials
- MongoDB Atlas cluster (connection URI)
- Docker image pushed to ECR

## Directory Structure

```
terraform/
├── main.tf                 # Main configuration
├── variables.tf            # Variable definitions
├── outputs.tf              # Output definitions
└── modules/
    ├── networking/         # VPC, subnets, NAT gateways
    ├── security/          # Security groups
    ├── alb/               # Application Load Balancer
    ├── ecs/               # ECS cluster, task definition, service
    ├── ecr/               # ECR repository
    ├── iam/               # IAM roles and policies
    └── logging/           # CloudWatch logging
```

## Deployment Guide

### 1. Prepare MongoDB Atlas

1. Create a MongoDB Atlas cluster
2. Create a database user with appropriate permissions
3. Whitelist AWS Fargate security group CIDR (or use IP whitelist)
4. Get the connection URI: `mongodb+srv://user:password@cluster.mongodb.net/database?retryWrites=true&w=majority`

### 2. Build and Push Docker Image

```bash
# Build image
docker build -t antonie-books:latest .

# Tag for ECR (after creating ECR repo via Terraform apply)
docker tag antonie-books:latest <account-id>.dkr.ecr.<region>.amazonaws.com/antonie-books-api:latest

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com

# Push image
docker push <account-id>.dkr.ecr.<region>.amazonaws.com/antonie-books-api:latest
```

### 3. Initialize Terraform

```bash
terraform init
```

### 4. Create terraform.tfvars

```hcl
aws_region        = "us-east-1"
container_image   = "<account-id>.dkr.ecr.us-east-1.amazonaws.com/antonie-books-api:latest"
mongodb_atlas_uri = "mongodb+srv://user:password@cluster.mongodb.net/antonie_books?retryWrites=true&w=majority"
```

**IMPORTANT:** Never commit `terraform.tfvars` with real credentials. Use environment variables instead:

```bash
export TF_VAR_mongodb_atlas_uri="mongodb+srv://..."
export TF_VAR_container_image="<image-uri>"
```

### 5. Plan and Apply

```bash
# Review changes
terraform plan

# Apply infrastructure
terraform apply
```

### 6. Access the Application

After deployment completes, get the ALB DNS name:

```bash
terraform output alb_dns_name
```

Access via: `http://<alb-dns-name>/docs`

## Infrastructure Components

### VPC and Networking
- **VPC CIDR:** 10.0.0.0/16 (configurable)
- **Public Subnets:** 2 subnets across availability zones
- **Private Subnets:** 2 subnets across availability zones
- **NAT Gateways:** 1 per AZ for outbound traffic
- **Internet Gateway:** For ingress from Internet

### Security Groups
- **ALB:** Allows HTTP (80) and HTTPS (443) from 0.0.0.0/0
- **ECS:** Allows container port (8000) from ALB only

### Application Load Balancer
- **Type:** Application Load Balancer
- **Target Group:** ECS tasks (IP target type)
- **Health Check:** `/health` endpoint every 30s
- **Listener:** HTTP port 80 (can be extended for HTTPS)

### ECS Fargate
- **Cluster:** Auto Scaling enabled with CloudWatch monitoring
- **Task Definition:**
  - CPU: 512 (configurable)
  - Memory: 1024 MB (configurable)
  - Desired Count: 2 (for high availability)
- **Auto Scaling:**
  - Scales based on CPU utilization (target: 70%)
  - Scales based on memory utilization (target: 80%)
  - Min: 1, Max: 4 tasks

### Container Configuration
- **Image Source:** ECR repository
- **Port:** 8000 (FastAPI)
- **Environment Variables:**
  - `ENVIRONMENT`
  - `DATABASE_NAME`
  - `API_HOST`
  - `API_PORT`
- **Secrets:**
  - `MONGO_URI` (stored in AWS Secrets Manager)
- **Logging:** CloudWatch Logs (group: `/ecs/antonie-books`)
- **Health Check:** Curl to `/health` endpoint

### MongoDB Connection
- **Assumption:** MongoDB Atlas (managed cloud service)
- **Connection:** Via Secrets Manager for secure credential storage
- **Security:** Fargate tasks can reach MongoDB via NAT gateway outbound
- **Best Practice:** Whitelist ALB security group in MongoDB network access

### ECR Repository
- **Auto Scanning:** Images scanned for vulnerabilities on push
- **Lifecycle Policy:** Keeps 10 latest tagged images, removes untagged after 7 days

### Logging
- **CloudWatch Logs:** `/ecs/antonie-books`
- **Retention:** 30 days
- **Access:** Via AWS Console or CLI

## Scaling Configuration

The service uses target tracking auto-scaling:

```hcl
# CPU-based scaling
target_value = 70.0 (ECSServiceAverageCPUUtilization)

# Memory-based scaling
target_value = 80.0 (ECSServiceAverageMemoryUtilization)

# Task count: 1-4
```

Modify in `terraform/modules/ecs/main.tf`.

## Destroying Infrastructure

```bash
terraform destroy
```

**WARNING:** This will delete all resources. Ensure MongoDB backups exist.

## Costs

Estimated monthly costs (rough):

| Component | Quantity | Cost |
|-----------|----------|------|
| ALB | 1 | ~$16 |
| Fargate | 2 tasks, 512 CPU, 1GB RAM | ~$30 |
| NAT Gateway | 2 | ~$32 |
| Data Transfer | Varies | $0.02/GB |
| CloudWatch Logs | ~30GB/month | ~$15 |
| **Total** | | **~$93** |

Use `terraform plan` to estimate exact costs.

## Security Best Practices

1. **MongoDB Connection:**
   - Use IAM database authentication if available
   - Whitelist specific IP ranges
   - Use VPC peering for on-premises access

2. **Secrets Management:**
   - Store `MONGO_URI` in Secrets Manager (done automatically)
   - Rotate credentials regularly
   - Never commit secrets to Git

3. **Network Security:**
   - ALB in public subnets
   - ECS tasks in private subnets
   - Use VPN/SSM Session Manager for container access

4. **Image Security:**
   - Use specific image tags (not `:latest`)
   - Scan images for vulnerabilities
   - Use private ECR repository

## Monitoring and Observability

### CloudWatch Metrics
- CPU utilization
- Memory utilization
- Network in/out
- Task count

### Logs
View logs:
```bash
aws logs tail /ecs/antonie-books --follow
```

### Health Checks
ALB monitors ECS task health via `/health` endpoint.

## Updating the Application

1. Build new Docker image
2. Push to ECR with new tag
3. Update `terraform.tfvars` with new image URI
4. Run `terraform apply`
5. ECS automatically updates task definition and deploys

## Troubleshooting

### Task fails to start
```bash
# Check logs
aws logs tail /ecs/antonie-books --follow

# Check task status
aws ecs describe-tasks --cluster antonie-books-cluster --tasks <task-id>
```

### ALB not routing to tasks
- Verify security groups allow port 8000
- Check target group health: `aws elbv2 describe-target-health`
- Ensure task `/health` endpoint responds with 200

### Cannot connect to MongoDB Atlas
- Verify network access is configured
- Check MONGO_URI in Secrets Manager
- Ensure Fargate NAT gateway can reach MongoDB

## Advanced: HTTPS/TLS

To add HTTPS:

1. Create or import ACM certificate
2. Update ALB listener to use HTTPS:443
3. Add HTTP->HTTPS redirect

See `modules/alb/main.tf` for listener configuration.

## Advanced: Custom Domain

1. Create Route53 hosted zone
2. Add alias record pointing to ALB DNS name
3. Update ALB certificate to include domain

## References

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest)
- [ECS Task Definition Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ecs-taskdefinition.html)
- [Fargate Pricing](https://aws.amazon.com/fargate/pricing/)
- [MongoDB Atlas Security](https://docs.atlas.mongodb.com/security/)
