"""
Terraform Variables Generator
Generates terraform.tfvars file based on user answers
"""
import os
import re
from typing import Dict, List, Any
from llm_manager import LLMManager
from terraform_parser import TerraformTemplateParser
from config import TEMPLATE_DIR, GENERATED_TERRAFORM_FILE

class TerraformGenerator:
    """Generates Terraform variables file based on user responses"""
    
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager
        self.output_file = os.path.join(TEMPLATE_DIR, GENERATED_TERRAFORM_FILE)
        
    def generate_terraform_vars_gpt4(self, answers: Dict[str, str], terraform_parser: TerraformTemplateParser = None):
        """Generate terraform.tfvars using GPT-4.1 based on user answers"""
        print("\n🤖 Generating Terraform variables using GPT-4.1...")
        
        # Get template analysis if parser provided
        template_context = ""
        if terraform_parser:
            analysis = terraform_parser.analyze_template()
            template_context = self._create_template_context(analysis)
        
        # Create prompt for GPT-4
        prompt = self._create_terraform_generation_prompt(answers, template_context)
        
        # Generate using GPT-4
        llm = self.llm_manager.get_gpt4_llm()
        response = llm.invoke(prompt)
        
        # Parse and format the response
        terraform_vars = self._parse_terraform_response(response.content)
        
        # Save to file
        self._save_terraform_vars(terraform_vars)
        
        print(f"✅ Terraform variables generated: {self.output_file}")
        return self.output_file
    
    def _create_terraform_generation_prompt(self, answers: Dict[str, str], template_context: str) -> str:
        """Create prompt for Terraform variables generation"""
        
        answers_text = "\n".join([f"{key}: {value}" for key, value in answers.items()])
        
        prompt = f"""
As an AWS Deployment Engineer expert, generate a terraform.tfvars file based on the user's requirements and the available Terraform template.

TERRAFORM TEMPLATE CONTEXT:
{template_context}

USER ANSWERS:
{answers_text}

REQUIREMENTS:
1. Generate a complete terraform.tfvars file with appropriate values
2. Map user answers to the correct Terraform variable names
3. Use AWS best practices for naming, security, and configuration
4. Include comments explaining the purpose of each variable
5. Set appropriate default values where the user didn't specify
6. Ensure security best practices (strong passwords, encryption enabled, etc.)
7. Use proper Terraform syntax for different variable types (strings, booleans, lists, maps)
8. Consider the target environment (dev/staging/prod) when setting values

VARIABLE TYPES TO HANDLE:
- Strings: Use quotes
- Numbers: No quotes
- Booleans: true/false (no quotes)
- Lists: ["item1", "item2"]
- Maps: {{key1 = "value1", key2 = "value2"}}

SECURITY CONSIDERATIONS:
- Generate strong random passwords for databases
- Enable encryption by default
- Use restrictive security group rules
- Enable deletion protection for production resources
- Follow principle of least privilege

OUTPUT FORMAT:
Generate only the terraform.tfvars file content with:
- Header comment explaining the file
- Well-organized sections by AWS service
- Inline comments for each variable
- Proper Terraform syntax

Example format:
```
# Terraform Variables File
# Generated for AWS Infrastructure Deployment

# General Configuration
aws_region = "us-east-1"
project_name = "my-project"

# VPC Configuration  
create_vpc = true
vpc_cidr = "10.0.0.0/16"

# EC2 Configuration
create_ec2 = true
ec2_instance_type = "t3.micro"
```

Generate the complete terraform.tfvars file now:
"""
        return prompt
    
    def _create_template_context(self, analysis: Dict) -> str:
        """Create template context for the prompt"""
        context_parts = []
        
        # Available variables
        context_parts.append("AVAILABLE TERRAFORM VARIABLES:")
        for category, variables in analysis.get('categories', {}).items():
            context_parts.append(f"\n{category}:")
            for var_name in variables[:10]:  # Limit to first 10 per category
                var_info = analysis['variables'].get(var_name, {})
                var_type = var_info.get('type', 'string')
                description = var_info.get('description', '')
                default = var_info.get('default')
                
                context_parts.append(f"  - {var_name} ({var_type}): {description}")
                if default is not None:
                    context_parts.append(f"    Default: {default}")
        
        # Service toggles
        conditional = analysis.get('conditional', {})
        if conditional:
            context_parts.append("\nSERVICE TOGGLES (create_* variables):")
            for service in conditional.keys():
                context_parts.append(f"  - create_{service}: Enable/disable {service.upper()} resources")
        
        return '\n'.join(context_parts)
    
    def _parse_terraform_response(self, response: str) -> str:
        """Parse and clean the GPT-4 response"""
        # Remove markdown code blocks if present
        response = re.sub(r'```[\w]*\n', '', response)
        response = re.sub(r'\n```', '', response)
        
        # Clean up any unwanted prefixes/suffixes
        lines = response.split('\n')
        cleaned_lines = []
        
        in_content = False
        for line in lines:
            # Start capturing after we see variable assignments or comments
            if not in_content and (line.strip().startswith('#') or '=' in line):
                in_content = True
            
            if in_content:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def _save_terraform_vars(self, content: str):
        """Save the generated terraform.tfvars content to file"""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_terraform_vars_manual(self, answers: Dict[str, str], terraform_parser: TerraformTemplateParser) -> str:
        """Generate terraform.tfvars manually based on predefined mappings"""
        print("\n📝 Generating Terraform variables using rule-based approach...")
        
        # Start with header
        content = [
            "# Terraform Variables File",
            "# Generated for AWS Infrastructure Deployment",
            f"# Generated on: {self._get_current_timestamp()}",
            "",
        ]
        
        # Map answers to variables
        variable_mappings = self._create_variable_mappings(answers, terraform_parser)
        
        # Group by categories
        categories = terraform_parser.get_variable_categories()
        
        for category, variables in categories.items():
            content.append(f"# {category} Configuration")
            
            for var_name in variables:
                var_info = terraform_parser.get_variable_by_name(var_name)
                value = variable_mappings.get(var_name)
                
                if value is not None:
                    # Add description as comment
                    description = var_info.get('description', '')
                    if description:
                        content.append(f"# {description}")
                    
                    # Add variable assignment
                    content.append(f"{var_name} = {self._format_terraform_value(value, var_info.get('type', 'string'))}")
                    content.append("")
        
        terraform_content = '\n'.join(content)
        self._save_terraform_vars(terraform_content)
        
        print(f"✅ Terraform variables generated: {self.output_file}")
        return self.output_file
    
    def _create_variable_mappings(self, answers: Dict[str, str], terraform_parser: TerraformTemplateParser) -> Dict[str, Any]:
        """Create mappings from user answers to Terraform variables"""
        mappings = {}
        
        # Start with default values from template
        for var_name, var_info in terraform_parser.variables.items():
            default = var_info.get('default')
            if default is not None:
                mappings[var_name] = default
        
        # Override with user preferences based on answers
        answer_text = ' '.join(answers.values()).lower()
        
        # Basic mappings based on common patterns
        if 'vpc' in answer_text or 'network' in answer_text:
            mappings['create_vpc'] = True
        
        if 'ec2' in answer_text or 'server' in answer_text or 'instance' in answer_text:
            mappings['create_ec2'] = True
            
        if 'database' in answer_text or 'mysql' in answer_text or 'postgres' in answer_text:
            mappings['create_rds'] = True
            
        if 'load balancer' in answer_text or 'alb' in answer_text:
            mappings['create_alb'] = True
            
        if 's3' in answer_text or 'storage' in answer_text or 'bucket' in answer_text:
            mappings['create_s3'] = True
            
        if 'kubernetes' in answer_text or 'eks' in answer_text:
            mappings['create_eks'] = True
            
        if 'lambda' in answer_text or 'serverless' in answer_text:
            mappings['create_lambda'] = True
        
        # Extract specific values
        for answer_key, answer_value in answers.items():
            if 'region' in answer_value.lower():
                # Try to extract AWS region
                regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
                for region in regions:
                    if region in answer_value:
                        mappings['aws_region'] = region
                        break
            
            if 'project' in answer_value.lower() or 'name' in answer_value.lower():
                # Extract project name
                words = answer_value.split()
                if len(words) >= 2:
                    mappings['project_name'] = '-'.join(words[-2:]).lower()
        
        return mappings
    
    def _format_terraform_value(self, value: Any, var_type: str) -> str:
        """Format value according to Terraform syntax"""
        if 'bool' in var_type:
            return 'true' if value else 'false'
        elif 'number' in var_type:
            return str(value)
        elif 'list' in var_type:
            if isinstance(value, list):
                formatted_items = [f'"{item}"' for item in value]
                return f"[{', '.join(formatted_items)}]"
            else:
                return f'["{value}"]'
        elif 'map' in var_type or 'object' in var_type:
            if isinstance(value, dict):
                formatted_pairs = [f'{k} = "{v}"' for k, v in value.items()]
                return f"{{{', '.join(formatted_pairs)}}}"
            else:
                return f'{{default = "{value}"}}'
        else:
            # Default to string
            return f'"{value}"'
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for file header"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def validate_generated_file(self) -> bool:
        """Validate the generated terraform.tfvars file"""
        if not os.path.exists(self.output_file):
            return False
        
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic validation checks
            if not content.strip():
                return False
            
            # Check for valid variable assignments
            assignments = [line for line in content.split('\n') if '=' in line and not line.strip().startswith('#')]
            
            return len(assignments) > 0
        
        except Exception as e:
            print(f"❌ Error validating file: {e}")
            return False
