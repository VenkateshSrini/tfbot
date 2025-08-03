"""
Terraform Template Parser
Parses Terraform files to extract variables and their metadata
"""
import os
import re
from typing import Dict, List, Set
from config import TEMPLATE_DIR, TF_VARIABLES_FILE, TF_MAIN_FILE

class TerraformTemplateParser:
    """Parser for Terraform templates to extract variables and dependencies"""
    
    def __init__(self):
        self.template_dir = TEMPLATE_DIR
        self.variables = {}
        self.resources = {}
        self.dependencies = {}
        
    def parse_variables_file(self) -> Dict:
        """Parse variables.tf file to extract variable definitions"""
        variables_file = os.path.join(self.template_dir, TF_VARIABLES_FILE)
        
        if not os.path.exists(variables_file):
            print(f"Variables file not found: {variables_file}")
            return {}
        
        with open(variables_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse variable blocks
        variable_blocks = re.findall(r'variable\s+"([^"]+)"\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}', content, re.DOTALL)
        
        for var_name, var_content in variable_blocks:
            var_info = self._parse_variable_block(var_name, var_content)
            self.variables[var_name] = var_info
        
        return self.variables
    
    def _parse_variable_block(self, var_name: str, content: str) -> Dict:
        """Parse individual variable block content"""
        var_info = {
            'name': var_name,
            'description': '',
            'type': 'string',
            'default': None,
            'sensitive': False,
            'required': True,
            'validation': None
        }
        
        # Extract description
        desc_match = re.search(r'description\s*=\s*"([^"]*)"', content)
        if desc_match:
            var_info['description'] = desc_match.group(1)
        
        # Extract type
        type_match = re.search(r'type\s*=\s*([^\n]+)', content)
        if type_match:
            var_info['type'] = type_match.group(1).strip()
        
        # Extract default value
        default_match = re.search(r'default\s*=\s*([^\n]+)', content)
        if default_match:
            default_value = default_match.group(1).strip()
            var_info['default'] = self._parse_default_value(default_value)
            var_info['required'] = False
        
        # Check if sensitive
        if 'sensitive' in content and 'true' in content:
            var_info['sensitive'] = True
        
        return var_info
    
    def _parse_default_value(self, value_str: str) -> any:
        """Parse default value from string representation"""
        value_str = value_str.strip()
        
        # Handle different types of values
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]  # String value
        elif value_str.lower() in ['true', 'false']:
            return value_str.lower() == 'true'  # Boolean value
        elif value_str.isdigit():
            return int(value_str)  # Integer value
        elif value_str.startswith('[') and value_str.endswith(']'):
            # List value - simplified parsing
            list_content = value_str[1:-1].strip()
            if not list_content:
                return []
            # Split by comma and clean up quotes
            items = [item.strip().strip('"') for item in list_content.split(',')]
            return items
        elif value_str.startswith('{') and value_str.endswith('}'):
            # Object/map value - simplified parsing
            return value_str  # Return as string for now
        else:
            return value_str
    
    def parse_main_file(self) -> Dict:
        """Parse main.tf file to extract resource information"""
        main_file = os.path.join(self.template_dir, TF_MAIN_FILE)
        
        if not os.path.exists(main_file):
            print(f"Main file not found: {main_file}")
            return {}
        
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract resource blocks
        resource_blocks = re.findall(r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{', content)
        
        for resource_type, resource_name in resource_blocks:
            resource_key = f"{resource_type}.{resource_name}"
            self.resources[resource_key] = {
                'type': resource_type,
                'name': resource_name,
                'aws_service': self._get_aws_service_from_type(resource_type)
            }
        
        return self.resources
    
    def _get_aws_service_from_type(self, resource_type: str) -> str:
        """Map Terraform resource type to AWS service"""
        service_mapping = {
            'aws_vpc': 'VPC',
            'aws_subnet': 'VPC',
            'aws_internet_gateway': 'VPC',
            'aws_route_table': 'VPC',
            'aws_security_group': 'VPC',
            'aws_instance': 'EC2',
            'aws_key_pair': 'EC2',
            'aws_lb': 'ELB',
            'aws_lb_target_group': 'ELB',
            'aws_lb_listener': 'ELB',
            'aws_db_instance': 'RDS',
            'aws_db_subnet_group': 'RDS',
            'aws_s3_bucket': 'S3',
            'aws_eks_cluster': 'EKS',
            'aws_iam_role': 'IAM',
            'aws_lambda_function': 'Lambda',
            'aws_cloudwatch_log_group': 'CloudWatch',
            'aws_eip': 'EC2',
            'aws_nat_gateway': 'VPC'
        }
        return service_mapping.get(resource_type, 'Unknown')
    
    def get_variable_categories(self) -> Dict[str, List[str]]:
        """Group variables by category/service"""
        categories = {
            'General': [],
            'VPC': [],
            'EC2': [],
            'Load Balancer': [],
            'RDS': [],
            'S3': [],
            'EKS': [],
            'Lambda': [],
            'CloudWatch': []
        }
        
        for var_name, var_info in self.variables.items():
            if any(keyword in var_name.lower() for keyword in ['project', 'region', 'tag']):
                categories['General'].append(var_name)
            elif any(keyword in var_name.lower() for keyword in ['vpc', 'subnet', 'igw', 'nat', 'route']):
                categories['VPC'].append(var_name)
            elif any(keyword in var_name.lower() for keyword in ['ec2', 'instance', 'key_pair', 'ami']):
                categories['EC2'].append(var_name)
            elif any(keyword in var_name.lower() for keyword in ['alb', 'load_balancer', 'target_group']):
                categories['Load Balancer'].append(var_name)
            elif any(keyword in var_name.lower() for keyword in ['rds', 'database', 'db_']):
                categories['RDS'].append(var_name)
            elif 's3' in var_name.lower():
                categories['S3'].append(var_name)
            elif 'eks' in var_name.lower():
                categories['EKS'].append(var_name)
            elif 'lambda' in var_name.lower():
                categories['Lambda'].append(var_name)
            elif 'cloudwatch' in var_name.lower():
                categories['CloudWatch'].append(var_name)
            else:
                categories['General'].append(var_name)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def get_conditional_variables(self) -> Dict[str, List[str]]:
        """Get variables that are conditional based on create_* flags"""
        conditional_vars = {}
        
        for var_name, var_info in self.variables.items():
            if var_name.startswith('create_'):
                service = var_name.replace('create_', '')
                conditional_vars[service] = []
                
                # Find related variables
                for other_var in self.variables.keys():
                    if service in other_var and not other_var.startswith('create_'):
                        conditional_vars[service].append(other_var)
        
        return conditional_vars
    
    def analyze_template(self) -> Dict:
        """Perform complete analysis of Terraform templates"""
        variables = self.parse_variables_file()
        resources = self.parse_main_file()
        categories = self.get_variable_categories()
        conditional = self.get_conditional_variables()
        
        return {
            'variables': variables,
            'resources': resources,
            'categories': categories,
            'conditional': conditional,
            'total_variables': len(variables),
            'total_resources': len(resources)
        }
    
    def get_variable_by_name(self, var_name: str) -> Dict:
        """Get specific variable information"""
        return self.variables.get(var_name, {})
    
    def get_required_variables(self) -> List[str]:
        """Get list of required variables (no default value)"""
        return [name for name, info in self.variables.items() if info.get('required', True)]
    
    def get_boolean_variables(self) -> List[str]:
        """Get list of boolean variables"""
        return [name for name, info in self.variables.items() if 'bool' in info.get('type', '')]
    
    def get_sensitive_variables(self) -> List[str]:
        """Get list of sensitive variables"""
        return [name for name, info in self.variables.items() if info.get('sensitive', False)]
