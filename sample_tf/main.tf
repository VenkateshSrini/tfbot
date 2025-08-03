# AWS Provider Configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = var.default_tags
  }
}

# Data sources for existing resources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# VPC and Networking Resources
resource "aws_vpc" "main" {
  count = var.create_vpc ? 1 : 0
  
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-vpc"
    Type = "VPC"
  })
}

resource "aws_internet_gateway" "main" {
  count = var.create_vpc && var.create_igw ? 1 : 0
  
  vpc_id = aws_vpc.main[0].id
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-igw"
    Type = "InternetGateway"
  })
}

resource "aws_subnet" "public" {
  count = var.create_vpc ? length(var.public_subnet_cidrs) : 0
  
  vpc_id                  = aws_vpc.main[0].id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = var.map_public_ip_on_launch
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-public-subnet-${count.index + 1}"
    Type = "PublicSubnet"
  })
}

resource "aws_subnet" "private" {
  count = var.create_vpc ? length(var.private_subnet_cidrs) : 0
  
  vpc_id            = aws_vpc.main[0].id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-private-subnet-${count.index + 1}"
    Type = "PrivateSubnet"
  })
}

resource "aws_route_table" "public" {
  count = var.create_vpc && var.create_igw ? 1 : 0
  
  vpc_id = aws_vpc.main[0].id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main[0].id
  }
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-public-rt"
    Type = "RouteTable"
  })
}

resource "aws_route_table_association" "public" {
  count = var.create_vpc && var.create_igw ? length(aws_subnet.public) : 0
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public[0].id
}

# NAT Gateway for private subnets
resource "aws_eip" "nat" {
  count = var.create_vpc && var.create_nat_gateway ? length(var.public_subnet_cidrs) : 0
  
  domain = "vpc"
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-nat-eip-${count.index + 1}"
    Type = "EIP"
  })
  
  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  count = var.create_vpc && var.create_nat_gateway ? length(var.public_subnet_cidrs) : 0
  
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-nat-gw-${count.index + 1}"
    Type = "NATGateway"
  })
}

resource "aws_route_table" "private" {
  count = var.create_vpc && var.create_nat_gateway ? length(var.private_subnet_cidrs) : 0
  
  vpc_id = aws_vpc.main[0].id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-private-rt-${count.index + 1}"
    Type = "RouteTable"
  })
}

resource "aws_route_table_association" "private" {
  count = var.create_vpc && var.create_nat_gateway ? length(aws_subnet.private) : 0
  
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# Security Groups
resource "aws_security_group" "web" {
  count = var.create_security_groups ? 1 : 0
  
  name_prefix = "${var.project_name}-web-"
  vpc_id      = var.create_vpc ? aws_vpc.main[0].id : var.existing_vpc_id
  description = "Security group for web servers"
  
  dynamic "ingress" {
    for_each = var.web_ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "All outbound traffic"
  }
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-web-sg"
    Type = "SecurityGroup"
  })
}

# EC2 Instances
resource "aws_key_pair" "main" {
  count = var.create_ec2 && var.ec2_key_pair_name != "" ? 1 : 0
  
  key_name   = var.ec2_key_pair_name
  public_key = var.ec2_public_key
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-keypair"
    Type = "KeyPair"
  })
}

resource "aws_instance" "web" {
  count = var.create_ec2 ? var.ec2_instance_count : 0
  
  ami                    = var.ec2_ami_id
  instance_type         = var.ec2_instance_type
  key_name              = var.create_ec2 && var.ec2_key_pair_name != "" ? aws_key_pair.main[0].key_name : var.existing_key_pair_name
  vpc_security_group_ids = var.create_security_groups ? [aws_security_group.web[0].id] : var.existing_security_group_ids
  subnet_id             = var.create_vpc ? aws_subnet.public[count.index % length(aws_subnet.public)].id : var.existing_subnet_ids[count.index % length(var.existing_subnet_ids)]
  
  user_data = var.ec2_user_data
  
  root_block_device {
    volume_type = var.ec2_volume_type
    volume_size = var.ec2_volume_size
    encrypted   = var.ec2_encrypt_volume
  }
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-web-${count.index + 1}"
    Type = "EC2Instance"
  })
}

# Application Load Balancer
resource "aws_lb" "main" {
  count = var.create_alb ? 1 : 0
  
  name               = "${var.project_name}-alb"
  internal           = var.alb_internal
  load_balancer_type = "application"
  security_groups    = var.create_security_groups ? [aws_security_group.web[0].id] : var.existing_security_group_ids
  subnets            = var.create_vpc ? aws_subnet.public[*].id : var.existing_subnet_ids
  
  enable_deletion_protection = var.alb_deletion_protection
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-alb"
    Type = "LoadBalancer"
  })
}

resource "aws_lb_target_group" "main" {
  count = var.create_alb ? 1 : 0
  
  name     = "${var.project_name}-tg"
  port     = var.alb_target_port
  protocol = var.alb_target_protocol
  vpc_id   = var.create_vpc ? aws_vpc.main[0].id : var.existing_vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = var.alb_health_check_healthy_threshold
    interval            = var.alb_health_check_interval
    matcher             = var.alb_health_check_matcher
    path                = var.alb_health_check_path
    port                = "traffic-port"
    protocol            = var.alb_target_protocol
    timeout             = var.alb_health_check_timeout
    unhealthy_threshold = var.alb_health_check_unhealthy_threshold
  }
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-tg"
    Type = "TargetGroup"
  })
}

resource "aws_lb_target_group_attachment" "main" {
  count = var.create_alb && var.create_ec2 ? var.ec2_instance_count : 0
  
  target_group_arn = aws_lb_target_group.main[0].arn
  target_id        = aws_instance.web[count.index].id
  port             = var.alb_target_port
}

resource "aws_lb_listener" "main" {
  count = var.create_alb ? 1 : 0
  
  load_balancer_arn = aws_lb.main[0].arn
  port              = var.alb_listener_port
  protocol          = var.alb_listener_protocol
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.main[0].arn
  }
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-listener"
    Type = "LoadBalancerListener"
  })
}

# RDS Database
resource "aws_db_subnet_group" "main" {
  count = var.create_rds ? 1 : 0
  
  name       = "${var.project_name}-db-subnet-group"
  subnet_ids = var.create_vpc ? aws_subnet.private[*].id : var.existing_private_subnet_ids
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-db-subnet-group"
    Type = "DBSubnetGroup"
  })
}

resource "aws_db_instance" "main" {
  count = var.create_rds ? 1 : 0
  
  identifier     = "${var.project_name}-database"
  engine         = var.rds_engine
  engine_version = var.rds_engine_version
  instance_class = var.rds_instance_class
  
  allocated_storage     = var.rds_allocated_storage
  max_allocated_storage = var.rds_max_allocated_storage
  storage_type          = var.rds_storage_type
  storage_encrypted     = var.rds_storage_encrypted
  
  db_name  = var.rds_database_name
  username = var.rds_username
  password = var.rds_password
  port     = var.rds_port
  
  vpc_security_group_ids = var.create_security_groups ? [aws_security_group.database[0].id] : var.existing_db_security_group_ids
  db_subnet_group_name   = aws_db_subnet_group.main[0].name
  
  backup_retention_period = var.rds_backup_retention_period
  backup_window          = var.rds_backup_window
  maintenance_window     = var.rds_maintenance_window
  
  skip_final_snapshot = var.rds_skip_final_snapshot
  deletion_protection = var.rds_deletion_protection
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-database"
    Type = "RDSInstance"
  })
}

# S3 Bucket
resource "aws_s3_bucket" "main" {
  count = var.create_s3 ? 1 : 0
  
  bucket = "${var.project_name}-${var.s3_bucket_suffix}"
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-bucket"
    Type = "S3Bucket"
  })
}

resource "aws_s3_bucket_versioning" "main" {
  count = var.create_s3 ? 1 : 0
  
  bucket = aws_s3_bucket.main[0].id
  versioning_configuration {
    status = var.s3_versioning_enabled ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  count = var.create_s3 ? 1 : 0
  
  bucket = aws_s3_bucket.main[0].id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = var.s3_encryption_algorithm
    }
  }
}

resource "aws_s3_bucket_public_access_block" "main" {
  count = var.create_s3 ? 1 : 0
  
  bucket = aws_s3_bucket.main[0].id
  
  block_public_acls       = var.s3_block_public_acls
  block_public_policy     = var.s3_block_public_policy
  ignore_public_acls      = var.s3_ignore_public_acls
  restrict_public_buckets = var.s3_restrict_public_buckets
}

# Lambda Function
resource "aws_iam_role" "lambda" {
  count = var.create_lambda ? 1 : 0
  
  name = "${var.project_name}-lambda-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-lambda-role"
    Type = "IAMRole"
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  count = var.create_lambda ? 1 : 0
  
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda[0].name
}

resource "aws_lambda_function" "main" {
  count = var.create_lambda ? 1 : 0
  
  filename         = var.lambda_filename
  function_name    = "${var.project_name}-lambda"
  role            = aws_iam_role.lambda[0].arn
  handler         = var.lambda_handler
  runtime         = var.lambda_runtime
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory_size
  
  environment {
    variables = var.lambda_environment_variables
  }
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-lambda"
    Type = "LambdaFunction"
  })
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "main" {
  count = var.create_cloudwatch_logs ? 1 : 0
  
  name              = "/aws/lambda/${var.project_name}"
  retention_in_days = var.cloudwatch_log_retention_days
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-log-group"
    Type = "CloudWatchLogGroup"
  })
}

# EKS Cluster
resource "aws_iam_role" "eks_cluster" {
  count = var.create_eks ? 1 : 0
  
  name = "${var.project_name}-eks-cluster-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
      }
    ]
  })
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-eks-cluster-role"
    Type = "IAMRole"
  })
}

resource "aws_iam_role_policy_attachment" "eks_cluster_policy" {
  count = var.create_eks ? 1 : 0
  
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks_cluster[0].name
}

resource "aws_eks_cluster" "main" {
  count = var.create_eks ? 1 : 0
  
  name     = "${var.project_name}-eks-cluster"
  role_arn = aws_iam_role.eks_cluster[0].arn
  version  = var.eks_cluster_version
  
  vpc_config {
    subnet_ids              = var.create_vpc ? concat(aws_subnet.public[*].id, aws_subnet.private[*].id) : var.existing_subnet_ids
    endpoint_private_access = var.eks_endpoint_private_access
    endpoint_public_access  = var.eks_endpoint_public_access
  }
  
  enabled_cluster_log_types = var.eks_cluster_log_types
  
  tags = merge(var.default_tags, {
    Name = "${var.project_name}-eks-cluster"
    Type = "EKSCluster"
  })
  
  depends_on = [aws_iam_role_policy_attachment.eks_cluster_policy]
}
