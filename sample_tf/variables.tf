# General Configuration
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name of the project (used for resource naming)"
  type        = string
  default     = "my-project"
}

variable "default_tags" {
  description = "Default tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Project     = "terraform-bot"
    ManagedBy   = "terraform"
  }
}

# VPC Configuration
variable "create_vpc" {
  description = "Whether to create a new VPC"
  type        = bool
  default     = true
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "enable_dns_hostnames" {
  description = "Enable DNS hostnames in the VPC"
  type        = bool
  default     = true
}

variable "enable_dns_support" {
  description = "Enable DNS support in the VPC"
  type        = bool
  default     = true
}

variable "existing_vpc_id" {
  description = "ID of existing VPC to use (if create_vpc is false)"
  type        = string
  default     = ""
}

# Internet Gateway Configuration
variable "create_igw" {
  description = "Whether to create an Internet Gateway"
  type        = bool
  default     = true
}

# Subnet Configuration
variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.10.0/24", "10.0.20.0/24"]
}

variable "map_public_ip_on_launch" {
  description = "Map public IP on launch for public subnets"
  type        = bool
  default     = true
}

variable "existing_subnet_ids" {
  description = "List of existing subnet IDs to use (if create_vpc is false)"
  type        = list(string)
  default     = []
}

variable "existing_private_subnet_ids" {
  description = "List of existing private subnet IDs for RDS"
  type        = list(string)
  default     = []
}

# NAT Gateway Configuration
variable "create_nat_gateway" {
  description = "Whether to create NAT Gateways for private subnets"
  type        = bool
  default     = true
}

# Security Group Configuration
variable "create_security_groups" {
  description = "Whether to create security groups"
  type        = bool
  default     = true
}

variable "web_ingress_rules" {
  description = "List of ingress rules for web security group"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTP"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS"
    },
    {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "SSH"
    }
  ]
}

variable "existing_security_group_ids" {
  description = "List of existing security group IDs to use"
  type        = list(string)
  default     = []
}

variable "existing_db_security_group_ids" {
  description = "List of existing security group IDs for database"
  type        = list(string)
  default     = []
}

# EC2 Configuration
variable "create_ec2" {
  description = "Whether to create EC2 instances"
  type        = bool
  default     = false
}

variable "ec2_instance_count" {
  description = "Number of EC2 instances to create"
  type        = number
  default     = 1
}

variable "ec2_instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "ec2_ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-0c02fb55956c7d316"  # Amazon Linux 2 in us-east-1
}

variable "ec2_key_pair_name" {
  description = "Name of the key pair for EC2 instances"
  type        = string
  default     = ""
}

variable "ec2_public_key" {
  description = "Public key content for EC2 key pair"
  type        = string
  default     = ""
}

variable "existing_key_pair_name" {
  description = "Name of existing key pair to use"
  type        = string
  default     = ""
}

variable "ec2_user_data" {
  description = "User data script for EC2 instances"
  type        = string
  default     = ""
}

variable "ec2_volume_type" {
  description = "Type of EBS volume for EC2 instances"
  type        = string
  default     = "gp3"
}

variable "ec2_volume_size" {
  description = "Size of EBS volume for EC2 instances (GB)"
  type        = number
  default     = 20
}

variable "ec2_encrypt_volume" {
  description = "Whether to encrypt EBS volumes"
  type        = bool
  default     = true
}

# Application Load Balancer Configuration
variable "create_alb" {
  description = "Whether to create an Application Load Balancer"
  type        = bool
  default     = false
}

variable "alb_internal" {
  description = "Whether the ALB is internal"
  type        = bool
  default     = false
}

variable "alb_deletion_protection" {
  description = "Enable deletion protection for ALB"
  type        = bool
  default     = false
}

variable "alb_target_port" {
  description = "Port for ALB target group"
  type        = number
  default     = 80
}

variable "alb_target_protocol" {
  description = "Protocol for ALB target group"
  type        = string
  default     = "HTTP"
}

variable "alb_listener_port" {
  description = "Port for ALB listener"
  type        = number
  default     = 80
}

variable "alb_listener_protocol" {
  description = "Protocol for ALB listener"
  type        = string
  default     = "HTTP"
}

variable "alb_health_check_healthy_threshold" {
  description = "Number of consecutive health checks successes required"
  type        = number
  default     = 2
}

variable "alb_health_check_interval" {
  description = "Interval between health checks (seconds)"
  type        = number
  default     = 30
}

variable "alb_health_check_matcher" {
  description = "Response codes to use when checking for a healthy response"
  type        = string
  default     = "200"
}

variable "alb_health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/"
}

variable "alb_health_check_timeout" {
  description = "Health check timeout (seconds)"
  type        = number
  default     = 5
}

variable "alb_health_check_unhealthy_threshold" {
  description = "Number of consecutive health check failures required"
  type        = number
  default     = 2
}

# RDS Configuration
variable "create_rds" {
  description = "Whether to create an RDS instance"
  type        = bool
  default     = false
}

variable "rds_engine" {
  description = "Database engine"
  type        = string
  default     = "mysql"
}

variable "rds_engine_version" {
  description = "Database engine version"
  type        = string
  default     = "8.0"
}

variable "rds_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "Allocated storage for RDS (GB)"
  type        = number
  default     = 20
}

variable "rds_max_allocated_storage" {
  description = "Maximum allocated storage for RDS (GB)"
  type        = number
  default     = 100
}

variable "rds_storage_type" {
  description = "Storage type for RDS"
  type        = string
  default     = "gp2"
}

variable "rds_storage_encrypted" {
  description = "Whether to encrypt RDS storage"
  type        = bool
  default     = true
}

variable "rds_database_name" {
  description = "Name of the database to create"
  type        = string
  default     = "mydb"
}

variable "rds_username" {
  description = "Username for the master DB user"
  type        = string
  default     = "admin"
}

variable "rds_password" {
  description = "Password for the master DB user"
  type        = string
  default     = "changeme123!"
  sensitive   = true
}

variable "rds_port" {
  description = "Port on which the DB accepts connections"
  type        = number
  default     = 3306
}

variable "rds_backup_retention_period" {
  description = "Backup retention period (days)"
  type        = number
  default     = 7
}

variable "rds_backup_window" {
  description = "Backup window"
  type        = string
  default     = "03:00-04:00"
}

variable "rds_maintenance_window" {
  description = "Maintenance window"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

variable "rds_skip_final_snapshot" {
  description = "Skip final snapshot when destroying RDS"
  type        = bool
  default     = true
}

variable "rds_deletion_protection" {
  description = "Enable deletion protection for RDS"
  type        = bool
  default     = false
}

# S3 Configuration
variable "create_s3" {
  description = "Whether to create an S3 bucket"
  type        = bool
  default     = false
}

variable "s3_bucket_suffix" {
  description = "Suffix for S3 bucket name (to ensure uniqueness)"
  type        = string
  default     = "data-bucket"
}

variable "s3_versioning_enabled" {
  description = "Enable versioning for S3 bucket"
  type        = bool
  default     = true
}

variable "s3_encryption_algorithm" {
  description = "Server-side encryption algorithm for S3"
  type        = string
  default     = "AES256"
}

variable "s3_block_public_acls" {
  description = "Block public ACLs for S3 bucket"
  type        = bool
  default     = true
}

variable "s3_block_public_policy" {
  description = "Block public policy for S3 bucket"
  type        = bool
  default     = true
}

variable "s3_ignore_public_acls" {
  description = "Ignore public ACLs for S3 bucket"
  type        = bool
  default     = true
}

variable "s3_restrict_public_buckets" {
  description = "Restrict public buckets for S3"
  type        = bool
  default     = true
}

# EKS Configuration
variable "create_eks" {
  description = "Whether to create an EKS cluster"
  type        = bool
  default     = false
}

variable "eks_cluster_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.28"
}

variable "eks_endpoint_private_access" {
  description = "Enable private API server endpoint"
  type        = bool
  default     = false
}

variable "eks_endpoint_public_access" {
  description = "Enable public API server endpoint"
  type        = bool
  default     = true
}

variable "eks_cluster_log_types" {
  description = "List of control plane logging to enable"
  type        = list(string)
  default     = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
}

# Lambda Configuration
variable "create_lambda" {
  description = "Whether to create a Lambda function"
  type        = bool
  default     = false
}

variable "lambda_filename" {
  description = "Path to the Lambda deployment package"
  type        = string
  default     = "lambda_function.zip"
}

variable "lambda_handler" {
  description = "Lambda function handler"
  type        = string
  default     = "index.handler"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.9"
}

variable "lambda_timeout" {
  description = "Lambda function timeout (seconds)"
  type        = number
  default     = 30
}

variable "lambda_memory_size" {
  description = "Lambda function memory size (MB)"
  type        = number
  default     = 128
}

variable "lambda_environment_variables" {
  description = "Environment variables for Lambda function"
  type        = map(string)
  default     = {}
}

# CloudWatch Configuration
variable "create_cloudwatch_logs" {
  description = "Whether to create CloudWatch log groups"
  type        = bool
  default     = false
}

variable "cloudwatch_log_retention_days" {
  description = "CloudWatch log retention period (days)"
  type        = number
  default     = 14
}
