"""
API Utilities for Terraform Bot API
Helper functions and utilities for the API
"""
import os
import sys
from typing import Dict, List

# Add parent directory to Python path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_service_descriptions() -> Dict[str, str]:
    """Get descriptions for AWS services"""
    return {
        'vpc': 'Virtual Private Cloud - Network isolation and routing for AWS resources',
        'ec2': 'Elastic Compute Cloud - Virtual servers and computing instances',
        'rds': 'Relational Database Service - Managed database instances',
        'lambda': 'AWS Lambda - Serverless computing functions',
        's3': 'Simple Storage Service - Object storage and static websites',
        'iam': 'Identity and Access Management - User and permission management',
        'cloudwatch': 'CloudWatch - Monitoring and logging services',
        'route53': 'Route 53 - DNS and domain management services',
        'apigateway': 'API Gateway - API management and routing',
        'cloudfront': 'CloudFront - Global content delivery network',
        'ecs': 'Elastic Container Service - Container orchestration',
        'eks': 'Elastic Kubernetes Service - Managed Kubernetes clusters',
        'elasticache': 'ElastiCache - In-memory caching services (Redis/Memcached)',
        'sns': 'Simple Notification Service - Messaging and notifications',
        'sqs': 'Simple Queue Service - Message queuing service',
        'secretsmanager': 'AWS Secrets Manager - Secure secret storage and rotation',
        'kms': 'Key Management Service - Encryption key management',
        'dynamodb': 'DynamoDB - NoSQL database service',
        'elb': 'Elastic Load Balancer - Load balancing for applications',
        'autoscaling': 'Auto Scaling - Automatic capacity management',
        'cloudformation': 'CloudFormation - Infrastructure as code',
        'elasticbeanstalk': 'Elastic Beanstalk - Application deployment platform'
    }

def generate_basic_questions_for_service(service: str) -> List[str]:
    """Generate basic questions for a service"""
    service = service.lower()
    
    questions_map = {
        'vpc': [
            "What CIDR block would you like for your VPC? (e.g., 10.0.0.0/16)",
            "How many availability zones do you want to use? (1-3 recommended)",
            "Do you need both public and private subnets?",
            "What is your project name for resource naming?"
        ],
        'ec2': [
            "What instance type do you need? (e.g., t3.micro, t3.small, t3.medium)",
            "How many instances do you want to launch initially?",
            "What operating system do you prefer? (Amazon Linux, Ubuntu, Windows)",
            "Do you need SSH/RDP access from the internet?",
            "What is the primary purpose of these instances?"
        ],
        'rds': [
            "What database engine do you prefer? (MySQL, PostgreSQL, Oracle, SQL Server)",
            "What instance class for your database? (db.t3.micro, db.t3.small, db.t3.medium)",
            "Do you need Multi-AZ deployment for high availability?",
            "What is the initial database storage size in GB?",
            "Do you need automated backups?"
        ],
        'lambda': [
            "What runtime environment do you need? (Python, Node.js, Java, .NET)",
            "What is the expected memory requirement? (128MB - 10GB)",
            "What will trigger your Lambda function? (API Gateway, S3, EventBridge)",
            "What is the expected execution timeout? (1-900 seconds)",
            "Do you need VPC access from your function?"
        ],
        's3': [
            "What type of storage access pattern? (Standard, Infrequent Access, Archive)",
            "Do you need versioning enabled for your objects?",
            "Do you need public read access or will this be a private bucket?",
            "Do you need server-side encryption?",
            "What is the primary use case? (Static website, data backup, application storage)"
        ],
        'iam': [
            "Do you need to create IAM users or just roles?",
            "What services will need access permissions?",
            "Do you need cross-account access capabilities?",
            "What level of access control do you require? (Read-only, Admin, Custom)"
        ],
        'cloudwatch': [
            "What metrics do you want to monitor?",
            "Do you need custom dashboards?",
            "What alert thresholds should trigger notifications?",
            "How long should logs be retained?"
        ],
        'route53': [
            "Do you have an existing domain name?",
            "Do you need DNS failover capabilities?",
            "What type of routing policy? (Simple, Weighted, Latency-based)",
            "Do you need health checks for your endpoints?"
        ]
    }
    
    default_questions = [
        f"What is the primary use case for {service.upper()}?",
        f"What capacity or size requirements do you have?",
        f"What environment is this for? (development, staging, production)",
        f"Do you have any specific security or compliance requirements?"
    ]
    
    return questions_map.get(service, default_questions)

def validate_service_name(service: str, available_services: List[str]) -> bool:
    """Validate if service name is available"""
    return service.upper() in [s.upper() for s in available_services]

def format_qa_pairs_for_terraform_generator(qa_pairs: List[Dict]) -> Dict:
    """Format Q&A pairs for terraform generator"""
    formatted_answers = {}
    
    for i, qa in enumerate(qa_pairs):
        # Create a unique key for each Q&A pair
        key = f"question_{i+1}"
        formatted_answers[key] = {
            'question': qa.get('question', ''),
            'answer': qa.get('answer', '')
        }
    
    return formatted_answers

def extract_services_from_analysis(analysis: Dict) -> List[str]:
    """Extract unique AWS services from template analysis"""
    services = set()
    
    if 'resources' in analysis:
        for resource_info in analysis['resources'].values():
            if 'aws_service' in resource_info:
                services.add(resource_info['aws_service'])
    
    return sorted(list(services))

def get_api_version() -> str:
    """Get API version"""
    return "1.0.0"

def get_api_info() -> Dict:
    """Get API information"""
    return {
        "message": "Terraform Bot API",
        "version": get_api_version(),
        "description": "AWS Infrastructure Deployment Automation API",
        "documentation": "/docs",
        "endpoints": {
            "GET /": "API information",
            "GET /services": "Get available AWS services",
            "POST /questions": "Get questions for selected services", 
            "POST /generate": "Generate Terraform vars file from Q&A pairs",
            "GET /health": "Health check"
        }
    }
