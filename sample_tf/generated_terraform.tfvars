# Terraform Variables File
# Generated for mycake-shop AWS Infrastructure Deployment
# SOC2 Compliance Configuration with EKS and S3 Integration

# ================================
# General Configuration
# ================================
aws_region = "us-east-1"                    # Primary AWS region for deployment
project_name = "mycake-shop"                # Project name used for resource naming and tagging

# SOC2 compliance tags for audit and governance
default_tags = {
  Project     = "mycake-shop"
  Environment = "production"
  Compliance  = "SOC2"
  Owner       = "DevOps-Team"
  ManagedBy   = "Terraform"
}

# ================================
# VPC Configuration
# ================================
create_vpc = true                           # Create new VPC for isolated network environment
vpc_cidr = "10.0.0.0/16"                   # VPC CIDR block providing 65,536 IP addresses
enable_dns_hostnames = true                # Enable DNS hostnames for EKS requirements
enable_dns_support = true                  # Enable DNS support for service discovery

# Public subnets for load balancers and NAT gateways (multi-AZ for HA)
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]

# Private subnets for EKS worker nodes and RDS (multi-AZ for HA)
private_subnet_cidrs = ["10.0.10.0/24", "10.0.20.0/24"]

# Internet Gateway and NAT Gateway for connectivity
create_igw = true                          # Internet Gateway for public subnet internet access
create_nat_gateway = true                  # NAT Gateway for private subnet outbound internet access
map_public_ip_on_launch = false           # Security best practice - no auto public IPs

# ================================
# Security Groups Configuration
# ================================
create_security_groups = true             # Create security groups for services

# Web tier security group rules (restrictive for SOC2 compliance)
web_ingress_rules = [
  {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTPS traffic from internet"
  },
  {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "HTTP traffic from internet (redirect to HTTPS)"
  }
]

# ================================
# EKS Configuration
# ================================
create_eks = true                          # Enable EKS cluster for container orchestration
eks_cluster_version = "1.28"              # Latest stable Kubernetes version
eks_endpoint_private_access = true        # Enable private API access for security
eks_endpoint_public_access = true         # Enable public API access for management
eks_cluster_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]  # Full logging for SOC2 compliance

# ================================
# S3 Configuration
# ================================
create_s3 = true                           # Enable S3 for PDF file storage
s3_bucket_suffix = "pdf-documents"         # Descriptive suffix for PDF storage bucket
s3_versioning_enabled = true               # Enable versioning for data protection and SOC2 compliance
s3_encryption_algorithm = "AES256"         # Server-side encryption for data at rest

# SOC2 compliant S3 security settings
s3_block_public_acls = true               # Block public ACLs for security
s3_block_public_policy = true             # Block public bucket policies
s3_ignore_public_acls = true              # Ignore public ACLs
s3_restrict_public_buckets = true         # Restrict public bucket access

# ================================
# CloudWatch Logs Configuration
# ================================
create_cloudwatch_logs = true             # Enable CloudWatch logs for monitoring and compliance
cloudwatch_log_retention_days = 90        # Extended retention for SOC2 audit requirements

# ================================
# Disabled Services
# ================================
# EC2 instances not needed with