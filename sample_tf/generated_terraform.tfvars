# Terraform Variables File
# Generated for AWS Infrastructure Deployment - My Cake Shop
# Configured for PCI-DSS compliance with S3 storage for PDF files and EKS integration

# ============================================================================
# GENERAL CONFIGURATION
# ============================================================================

# AWS region for resource deployment
aws_region = "us-east-1"

# Project name used for resource naming and tagging
project_name = "my-cake-shop"

# Default tags applied to all resources for compliance and management
default_tags = {
  Project     = "my-cake-shop"
  Environment = "production"
  Compliance  = "PCI-DSS"
  Owner       = "cake-shop-team"
  ManagedBy   = "terraform"
}

# ============================================================================
# VPC CONFIGURATION
# ============================================================================

# Create new VPC for isolated network environment
create_vpc = true

# VPC CIDR block - using /16 for sufficient IP space
vpc_cidr = "10.0.0.0/16"

# Enable DNS features for proper service discovery
enable_dns_hostnames = true
enable_dns_support = true

# Public subnet CIDRs across multiple AZs for high availability
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]

# Private subnet CIDRs for secure backend resources
private_subnet_cidrs = ["10.0.10.0/24", "10.0.20.0/24"]

# Create Internet Gateway for public internet access
create_igw = true

# Create NAT Gateway for private subnet internet access
create_nat_gateway = true

# Auto-assign public IPs to instances in public subnets
map_public_ip_on_launch = true

# ============================================================================
# SECURITY GROUP CONFIGURATION
# ============================================================================

# Create security groups for network access control
create_security_groups = true

# Web security group ingress rules for PCI-DSS compliance
web_ingress_rules = [
  {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS traffic for secure web access"
  },
  {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP traffic (redirect to HTTPS)"
  }
]

# No existing security groups to import
existing_security_group_ids = []

# ============================================================================
# EC2 CONFIGURATION
# ============================================================================

# Disable standalone EC2 instances (using EKS instead)
create_ec2 = false

# EC2 configuration (kept for potential future use)
ec2_instance_count = 0
ec2_instance_type = "t3.medium"
ec2_ami_id = "ami-0c02fb55956c7d316"
ec2_key_pair_name = ""
ec2_volume_type = "gp3"
ec2_volume_size = 30

# ============================================================================
# LOAD BALANCER CONFIGURATION
# ============================================================================

# Create ALB for EKS ingress traffic distribution
create_alb = true

# External-facing ALB for public access
alb_internal = false

# Enable deletion protection for production environment
alb_deletion_protection = true

# ALB target configuration for HTTPS traffic
alb_target_port = 80
alb_target_protocol = "HTTP"
alb_listener_port = 443
alb_listener_protocol = "HTTPS"

# Health check configuration for high availability
alb_health_check_healthy_threshold = 3
alb_health_check_interval = 30
alb_health_check_matcher = "200,301,302"

# ============================================================================
# RDS CONFIGURATION
# ============================================================================

# Enable RDS for application database needs
create_rds = true

# MySQL engine for cake shop application
rds_engine = "mysql"
rds_engine_version = "8.0"

# Storage configuration with auto-scaling
rds_allocated_storage = 50
rds_max_allocated_storage =