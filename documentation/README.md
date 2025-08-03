# Terraform Bot (tf-bot)

🚀 **AWS Infrastructure Deployment Automation Tool**

Terraform Bot is an AI-powered tool that simplifies AWS infrastructure deployment by automatically generating Terraform configurations based on your requirements. Similar to helm-bot for Kubernetes, tf-bot helps you deploy AWS resources through intelligent questioning and automated Terraform code generation.

## 🌟 Features

- **🤖 AI-Powered**: Uses GPT-4 to generate intelligent questions and Terraform configurations
- **☁️ Multi-Service Support**: Supports 50+ AWS services including VPC, EC2, RDS, S3, EKS, Lambda, and more
- **📋 Interactive Questionnaire**: Asks relevant questions based on your infrastructure needs
- **🔧 Smart Generation**: Creates production-ready `terraform.tfvars` files
- **🛡️ Security Best Practices**: Implements AWS security best practices by default
- **🎯 Template-Based**: Uses comprehensive Terraform templates covering most AWS use cases

## 🏗️ Supported AWS Services

| Category | Services |
|----------|----------|
| **Networking** | VPC, Subnets, Internet Gateway, NAT Gateway, Route Tables, Security Groups |
| **Compute** | EC2 Instances, Key Pairs, Elastic Load Balancer (ALB) |
| **Database** | RDS (MySQL, PostgreSQL, etc.) |
| **Storage** | S3 Buckets with encryption and versioning |
| **Container** | EKS Clusters with IAM roles |
| **Serverless** | Lambda Functions with IAM roles |
| **Monitoring** | CloudWatch Log Groups |
| **Security** | IAM Roles and Policies |

## 📋 Prerequisites

- Python 3.8+
- OpenAI API Key
- AWS CLI configured (for deployment)
- Terraform installed (for deployment)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the tfbot directory
cd tfbot

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Terraform Bot

```bash
python tf-bot.py
```

### 3. Follow the Interactive Process

1. **Template Analysis**: The bot analyzes the Terraform templates
2. **Question Generation**: AI generates relevant questions based on available resources
3. **Answer Collection**: You answer questions about your infrastructure needs
4. **Configuration Generation**: AI creates a `terraform.tfvars` file
5. **Ready to Deploy**: Use standard Terraform commands to deploy

### 4. Deploy Your Infrastructure

```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Deploy to AWS
terraform apply
```

## 📁 Project Structure

```
tfbot/
├── tf-bot.py                    # Main application
├── config.py                    # Configuration settings
├── terraform_parser.py          # Terraform template parser
├── llm_manager.py              # OpenAI LLM manager
├── terraform_question_manager.py # Question generation and collection
├── terraform_generator.py       # Terraform vars generator
├── requirements.txt             # Python dependencies
└── sample_tf/                  # Terraform templates
    ├── main.tf                 # Main infrastructure resources
    ├── variables.tf            # Variable definitions
    ├── outputs.tf              # Output definitions
    ├── lambda_function.py      # Sample Lambda function
    ├── generated_questions.txt # Generated questions (auto-created)
    └── generated_terraform.tfvars # Generated config (auto-created)
```

## 🎯 Example Usage Scenarios

### Scenario 1: Simple Web Application
- VPC with public/private subnets
- EC2 instances with load balancer
- RDS database
- S3 bucket for static assets

### Scenario 2: Microservices on EKS
- VPC with multiple availability zones
- EKS cluster with managed node groups
- Application Load Balancer
- CloudWatch for monitoring

### Scenario 3: Serverless Application
- Lambda functions
- S3 buckets for storage
- CloudWatch for logging
- IAM roles and policies

## 🔧 Configuration Options

The bot will ask about:

- **AWS Region**: Where to deploy resources
- **Project Name**: For resource naming and tagging
- **Environment**: Development, staging, or production
- **Network Configuration**: VPC CIDR, subnet layouts
- **Security Settings**: Security groups, encryption preferences
- **Scaling Requirements**: Instance types, auto-scaling preferences
- **Backup and Monitoring**: Backup policies, logging requirements

## 🛡️ Security Features

- **Encryption by Default**: All storage encrypted
- **Secure Networking**: Private subnets for databases
- **IAM Best Practices**: Least privilege access
- **Security Groups**: Restrictive ingress rules
- **Backup Policies**: Automated backup configuration

## 📊 Template Information

View template details:

```bash
python tf-bot.py --info
```

This shows:
- Available variables (100+ configuration options)
- Supported AWS services
- Variable categories and dependencies

## 🤝 Integration with Existing Infrastructure

The generated Terraform can be:
- **Standalone**: Deploy complete new infrastructure
- **Modular**: Integrate with existing Terraform modules
- **Customizable**: Modify generated files as needed

## 🔄 Workflow Integration

1. **Development**: Generate dev environment configurations
2. **Testing**: Create isolated test environments
3. **Production**: Deploy production-ready infrastructure
4. **CI/CD**: Integrate with deployment pipelines

## 📝 Generated Files

### `generated_terraform.tfvars`
Contains all variable assignments based on your answers:

```hcl
# General Configuration
aws_region = "us-east-1"
project_name = "my-web-app"

# VPC Configuration
create_vpc = true
vpc_cidr = "10.0.0.0/16"
public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]

# EC2 Configuration
create_ec2 = true
ec2_instance_type = "t3.medium"
ec2_instance_count = 2
```

## 🎛️ Advanced Usage

### Custom Templates
Modify files in `sample_tf/` to add new AWS services or change configurations.

### Environment-Specific Configurations
Generate different `.tfvars` files for different environments.

### Integration with Terraform Cloud
Use generated configurations with Terraform Cloud or Enterprise.

## 🔍 Troubleshooting

### Common Issues

1. **OpenAI API Key**: Ensure your API key is valid and has credits
2. **AWS Credentials**: Configure AWS CLI before deployment
3. **Terraform Version**: Use Terraform 1.0+ for best compatibility

### Getting Help

- Check generated questions in `sample_tf/generated_questions.txt`
- Review template analysis with `python tf-bot.py --info`
- Validate generated file before deployment

## 🚧 Roadmap

- [ ] Support for more AWS services (API Gateway, SQS, etc.)
- [ ] Terraform module generation
- [ ] Cost estimation integration
- [ ] Multi-region deployment support
- [ ] Terraform state management configuration

## 📄 License

This project follows the same license as the parent helm-bot project.

---

## 🤖 About Terraform Bot

Terraform Bot bridges the gap between infrastructure requirements and Terraform code, making AWS deployment accessible to both beginners and experts. By leveraging AI and AWS best practices, it ensures your infrastructure is secure, scalable, and maintainable.

**Ready to deploy to AWS? Run `python tf-bot.py` and let's get started!** 🚀
