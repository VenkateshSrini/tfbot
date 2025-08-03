# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = var.create_vpc ? aws_vpc.main[0].id : null
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = var.create_vpc ? aws_vpc.main[0].cidr_block : null
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = var.create_vpc && var.create_igw ? aws_internet_gateway.main[0].id : null
}

# Subnet Outputs
output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = var.create_vpc ? aws_subnet.public[*].id : []
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = var.create_vpc ? aws_subnet.private[*].id : []
}

output "public_subnet_cidrs" {
  description = "CIDR blocks of the public subnets"
  value       = var.create_vpc ? aws_subnet.public[*].cidr_block : []
}

output "private_subnet_cidrs" {
  description = "CIDR blocks of the private subnets"
  value       = var.create_vpc ? aws_subnet.private[*].cidr_block : []
}

# NAT Gateway Outputs
output "nat_gateway_ids" {
  description = "IDs of the NAT Gateways"
  value       = var.create_vpc && var.create_nat_gateway ? aws_nat_gateway.main[*].id : []
}

output "nat_gateway_public_ips" {
  description = "Public IPs of the NAT Gateways"
  value       = var.create_vpc && var.create_nat_gateway ? aws_eip.nat[*].public_ip : []
}

# Security Group Outputs
output "web_security_group_id" {
  description = "ID of the web security group"
  value       = var.create_security_groups ? aws_security_group.web[0].id : null
}

output "database_security_group_id" {
  description = "ID of the database security group"
  value       = var.create_security_groups && var.create_rds ? aws_security_group.database[0].id : null
}

# EC2 Outputs
output "ec2_instance_ids" {
  description = "IDs of the EC2 instances"
  value       = var.create_ec2 ? aws_instance.web[*].id : []
}

output "ec2_public_ips" {
  description = "Public IP addresses of the EC2 instances"
  value       = var.create_ec2 ? aws_instance.web[*].public_ip : []
}

output "ec2_private_ips" {
  description = "Private IP addresses of the EC2 instances"
  value       = var.create_ec2 ? aws_instance.web[*].private_ip : []
}

output "ec2_public_dns" {
  description = "Public DNS names of the EC2 instances"
  value       = var.create_ec2 ? aws_instance.web[*].public_dns : []
}

# Load Balancer Outputs
output "alb_dns_name" {
  description = "DNS name of the load balancer"
  value       = var.create_alb ? aws_lb.main[0].dns_name : null
}

output "alb_zone_id" {
  description = "Zone ID of the load balancer"
  value       = var.create_alb ? aws_lb.main[0].zone_id : null
}

output "alb_arn" {
  description = "ARN of the load balancer"
  value       = var.create_alb ? aws_lb.main[0].arn : null
}

output "target_group_arn" {
  description = "ARN of the target group"
  value       = var.create_alb ? aws_lb_target_group.main[0].arn : null
}

# RDS Outputs
output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = var.create_rds ? aws_db_instance.main[0].endpoint : null
  sensitive   = true
}

output "rds_port" {
  description = "RDS instance port"
  value       = var.create_rds ? aws_db_instance.main[0].port : null
}

output "rds_database_name" {
  description = "RDS database name"
  value       = var.create_rds ? aws_db_instance.main[0].db_name : null
}

output "rds_username" {
  description = "RDS master username"
  value       = var.create_rds ? aws_db_instance.main[0].username : null
  sensitive   = true
}

# S3 Outputs
output "s3_bucket_id" {
  description = "ID of the S3 bucket"
  value       = var.create_s3 ? aws_s3_bucket.main[0].id : null
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = var.create_s3 ? aws_s3_bucket.main[0].arn : null
}

output "s3_bucket_domain_name" {
  description = "Domain name of the S3 bucket"
  value       = var.create_s3 ? aws_s3_bucket.main[0].bucket_domain_name : null
}

# EKS Outputs
output "eks_cluster_id" {
  description = "Name of the EKS cluster"
  value       = var.create_eks ? aws_eks_cluster.main[0].name : null
}

output "eks_cluster_arn" {
  description = "ARN of the EKS cluster"
  value       = var.create_eks ? aws_eks_cluster.main[0].arn : null
}

output "eks_cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = var.create_eks ? aws_eks_cluster.main[0].endpoint : null
}

output "eks_cluster_version" {
  description = "Kubernetes server version for EKS cluster"
  value       = var.create_eks ? aws_eks_cluster.main[0].version : null
}

# Lambda Outputs
output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = var.create_lambda ? aws_lambda_function.main[0].function_name : null
}

output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = var.create_lambda ? aws_lambda_function.main[0].arn : null
}

output "lambda_invoke_arn" {
  description = "Invoke ARN of the Lambda function"
  value       = var.create_lambda ? aws_lambda_function.main[0].invoke_arn : null
}

# CloudWatch Outputs
output "cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = var.create_cloudwatch_logs ? aws_cloudwatch_log_group.main[0].name : null
}

output "cloudwatch_log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = var.create_cloudwatch_logs ? aws_cloudwatch_log_group.main[0].arn : null
}

# General Outputs
output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

output "aws_caller_identity" {
  description = "AWS caller identity"
  value       = data.aws_caller_identity.current
}
