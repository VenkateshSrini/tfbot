"""
Question Manager for Terraform Bot
Generates and manages questions based on Terraform template analysis
"""
import os
from typing import Dict, List
from terraform_parser import TerraformTemplateParser
from llm_manager import LLMManager
from config import GENERATED_QUESTIONS_FILE, TEMPLATE_DIR

class TerraformQuestionManager:
    """Manages question generation and collection for Terraform variables"""
    
    def __init__(self, llm_manager: LLMManager, terraform_parser: TerraformTemplateParser):
        self.llm_manager = llm_manager
        self.terraform_parser = terraform_parser
        self.questions_file = os.path.join(TEMPLATE_DIR, GENERATED_QUESTIONS_FILE)
        
    def ensure_questions_exist(self) -> str:
        """Ensure questions file exists, generate if needed"""
        if os.path.exists(self.questions_file):
            print(f"✅ Questions file already exists: {self.questions_file}")
            return self.questions_file
        
        print("📝 Generating questions from Terraform templates...")
        print("🔍 Analyzing Terraform templates...")
        analysis = self.terraform_parser.analyze_template()
        
        if not analysis['variables']:
            print("❌ No variables found in Terraform templates.")
            print("   Please ensure your Terraform files are in the 'sample_tf' directory.")
            return self.questions_file
        
        print(f"✅ Found {analysis['total_variables']} variables in {analysis['total_resources']} AWS resources")
        print(f"   AWS Services available: {', '.join(sorted(set(r['aws_service'] for r in analysis['resources'].values())))}")
        
        self.generate_questions_from_analysis(analysis)
        return self.questions_file
    
    def generate_questions_from_analysis(self, analysis: Dict):
        """Generate questions based on provided Terraform template analysis"""
        print(f"📊 Found {analysis['total_variables']} variables in {analysis['total_resources']} resources")
        
        # Generate questions using LLM
        service_questions = self._generate_questions_with_llm(analysis)
        
        # Save questions to file
        self._save_service_questions_to_file(service_questions)
        print(f"✅ Service-organized questions generated and saved to: {self.questions_file}")
    
    def generate_questions(self):
        """Generate questions based on Terraform template analysis (legacy method)"""
        print("🔍 Analyzing Terraform templates...")
        analysis = self.terraform_parser.analyze_template()
        
        if not analysis['variables']:
            print("❌ No variables found in Terraform templates.")
            return
        
        self.generate_questions_from_analysis(analysis)
    
    def _generate_questions_with_llm(self, analysis: Dict) -> Dict[str, List[str]]:
        """Generate service-organized questions using LLM based on template analysis"""
        
        # Create context for LLM
        context = self._create_llm_context(analysis)
        
        # Get available services from the template
        available_services = self._get_available_services(analysis)
        
        prompt = f"""
                    As an AWS Deployment Engineer expert, analyze the following Terraform template and generate service-organized questions to collect user requirements.

                    TERRAFORM TEMPLATE ANALYSIS:
                    {context}

                    AVAILABLE AWS SERVICES: {', '.join(available_services)}

                    REQUIREMENTS:
                    1. Organize questions by AWS service (Service-name: SERVICE_NAME, Questions: [list of questions])
                    2. Generate essential questions for each service that can achieve 98% configuration accuracy
                    3. Ask minimal but comprehensive questions to infer maximum details
                    4. Include service dependencies (e.g., VPC needed for EC2, RDS)
                    5. Make questions smart to infer related configurations

                    QUESTION FORMAT FOR EACH SERVICE:
                    Service-name: [SERVICE_NAME]
                    Questions:
                    - [Essential question 1]
                    - [Essential question 2]
                    - [Essential question 3]

                    GUIDELINES:
                    - Keep questions minimal but comprehensive
                    - Ask about naming patterns to infer multiple resource names
                    - Include environment context questions (dev/staging/prod)
                    - Ask about size/capacity to infer instance types and storage
                    - Include security and compliance essentials
                    - For VPC: Ask about network architecture and connectivity needs
                    - For EC2: Ask about application requirements and scale
                    - For RDS: Ask about database type, size, and backup needs
                    - For S3: Ask about storage type and access patterns
                    - For Lambda: Ask about runtime, triggers, and permissions
                    - For ALB: Ask about load balancing requirements and SSL
                    - For EKS: Ask about cluster size and workload types
                    - For CloudWatch: Ask about monitoring and alerting needs

                    Generate service-organized questions that will collect essential information efficiently.
                    """

        llm = self.llm_manager.get_default_llm()
        response = llm.invoke(prompt)
        
        # Parse the response into service-organized questions
        service_questions = self._parse_service_questions(response.content)
        return service_questions
    
    def _create_llm_context(self, analysis: Dict) -> str:
        """Create context string for LLM prompt"""
        context_parts = []
        
        # Variables summary
        context_parts.append(f"VARIABLES FOUND: {analysis['total_variables']}")
        context_parts.append(f"RESOURCES FOUND: {analysis['total_resources']}")
        
        # Categories
        if analysis['categories']:
            context_parts.append("\nVARIABLE CATEGORIES:")
            for category, variables in analysis['categories'].items():
                context_parts.append(f"  {category}: {', '.join(variables[:5])}{'...' if len(variables) > 5 else ''}")
        
        # Conditional services
        if analysis['conditional']:
            context_parts.append("\nCONDITIONAL SERVICES (can be enabled/disabled):")
            for service, related_vars in analysis['conditional'].items():
                context_parts.append(f"  {service.upper()}: {len(related_vars)} configuration variables")
        
        # Key variables
        required_vars = self.terraform_parser.get_required_variables()
        boolean_vars = self.terraform_parser.get_boolean_variables()
        sensitive_vars = self.terraform_parser.get_sensitive_variables()
        
        if required_vars:
            context_parts.append(f"\nREQUIRED VARIABLES: {', '.join(required_vars[:10])}")
        if boolean_vars:
            context_parts.append(f"BOOLEAN FLAGS: {', '.join(boolean_vars[:10])}")
        if sensitive_vars:
            context_parts.append(f"SENSITIVE VARIABLES: {', '.join(sensitive_vars)}")
        
        # Available AWS services
        aws_services = set()
        for resource_info in analysis['resources'].values():
            aws_services.add(resource_info['aws_service'])
        
        if aws_services:
            context_parts.append(f"\nAWS SERVICES SUPPORTED: {', '.join(sorted(aws_services))}")
        
        return '\n'.join(context_parts)
    
    def _get_available_services(self, analysis: Dict) -> List[str]:
        """Get list of available AWS services from the template"""
        services = set()
        
        # Get services from conditional variables (create_* flags)
        for service in analysis.get('conditional', {}).keys():
            services.add(service.upper())
        
        # Get services from resources
        for resource_info in analysis.get('resources', {}).values():
            services.add(resource_info['aws_service'])
        
        # Add general category
        services.add('GENERAL')
        
        return sorted(list(services))
    
    def _parse_service_questions(self, response: str) -> Dict[str, List[str]]:
        """Parse LLM response into service-organized questions"""
        lines = response.strip().split('\n')
        service_questions = {}
        current_service = None
        current_questions = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Check if line starts with "Service-name:"
            if line.startswith('Service-name:') or line.startswith('Service:'):
                # Save previous service questions
                if current_service and current_questions:
                    service_questions[current_service] = current_questions.copy()
                
                # Extract service name
                service_name = line.split(':', 1)[1].strip()
                current_service = service_name
                current_questions = []
                
            elif line.startswith('Questions:'):
                # Start of questions section
                continue
                
            elif line.startswith('- ') or line.startswith('• '):
                # Question item
                question = line.lstrip('- •').strip()
                if question and current_service:
                    current_questions.append(question)
        
        # Add the last service
        if current_service and current_questions:
            service_questions[current_service] = current_questions
        
        return service_questions
    
    def _parse_llm_response(self, response: str) -> List[str]:
        """Parse LLM response into individual questions"""
        lines = response.strip().split('\n')
        questions = []
        
        current_question = ""
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and headers
            if not line or line.startswith('#') or line.startswith('**'):
                if current_question:
                    questions.append(current_question.strip())
                    current_question = ""
                continue
            
            # Check if line starts with a number or bullet point (new question)
            if (line[0].isdigit() and '.' in line) or line.startswith('- ') or line.startswith('• '):
                if current_question:
                    questions.append(current_question.strip())
                current_question = line
            else:
                # Continue previous question
                if current_question:
                    current_question += " " + line
                else:
                    current_question = line
        
        # Add the last question
        if current_question:
            questions.append(current_question.strip())
        
        # Clean up questions
        cleaned_questions = []
        for q in questions:
            # Remove numbering and bullet points
            q = q.lstrip('0123456789.- •').strip()
            if q and '?' in q:  # Only keep actual questions
                cleaned_questions.append(q)
        
        return cleaned_questions
    
    def _save_service_questions_to_file(self, service_questions: Dict[str, List[str]]):
        """Save service-organized questions to file"""
        os.makedirs(os.path.dirname(self.questions_file), exist_ok=True)
        
        with open(self.questions_file, 'w', encoding='utf-8') as f:
            f.write("# Terraform AWS Infrastructure Questions (Service-Organized)\n")
            f.write("# Generated automatically based on template analysis\n\n")
            
            for service_name, questions in service_questions.items():
                f.write(f"Service-name: {service_name}\n")
                f.write("Questions:\n")
                for question in questions:
                    f.write(f"- {question}\n")
                f.write("\n")
    
    def _save_questions_to_file(self, questions: List[str]):
        """Save questions to file (legacy method)"""
        os.makedirs(os.path.dirname(self.questions_file), exist_ok=True)
        
        with open(self.questions_file, 'w', encoding='utf-8') as f:
            f.write("# Terraform AWS Infrastructure Questions\n")
            f.write("# Generated automatically based on template analysis\n\n")
            
            for i, question in enumerate(questions, 1):
                f.write(f"{i}. {question}\n\n")
    
    def collect_answers(self, questions_file: str) -> Dict[str, str]:
        """Collect answers from user using interactive service selection"""
        if not os.path.exists(questions_file):
            print(f"❌ Questions file not found: {questions_file}")
            return {}
        
        print("\n" + "="*60)
        print("🚀 TERRAFORM AWS INFRASTRUCTURE CONFIGURATION")
        print("="*60)
        
        # Parse service questions from file
        service_questions = self._parse_service_questions_from_file(questions_file)
        
        if not service_questions:
            print("❌ No service questions found in file")
            return {}
        
        # Show available services
        available_services = list(service_questions.keys())
        print(f"\n📋 Available AWS Services: {', '.join(available_services)}")
        
        # Ask which services to deploy
        selected_services = self._select_services(available_services)
        
        if not selected_services:
            print("❌ No services selected")
            return {}
        
        # Collect answers for selected services
        all_answers = {}
        
        # Always ask general questions first if available
        if 'GENERAL' in service_questions and 'GENERAL' not in selected_services:
            selected_services.insert(0, 'GENERAL')
        
        # Ask questions for each selected service
        for service in selected_services:
            if service in service_questions:
                print(f"\n🔧 Configuring {service} Service")
                print("-" * 40)
                
                service_answers = self._collect_service_answers(service, service_questions[service])
                
                # Add service prefix to avoid conflicts
                for key, value in service_answers.items():
                    all_answers[f"{service.lower()}_{key}"] = value
                
                # Infer additional configurations
                inferred_configs = self._infer_configurations(service, service_answers)
                all_answers.update(inferred_configs)
        
        print(f"\n✅ Configuration complete! Collected answers for {len(selected_services)} services")
        print(f"📊 Total configurations: {len(all_answers)}")
        
        return all_answers
    
    def _select_services(self, available_services: List[str]) -> List[str]:
        """Interactive service selection"""
        print("\n🎯 Which AWS services do you want to deploy?")
        print("💡 Enter service numbers separated by commas (e.g., 1,3,5) or 'all' for all services:")
        
        for i, service in enumerate(available_services, 1):
            print(f"   {i}. {service}")
        
        while True:
            selection = input("\n🔍 Your selection: ").strip().lower()
            
            if selection == 'all':
                return available_services.copy()
            
            try:
                if ',' in selection:
                    indices = [int(x.strip()) for x in selection.split(',')]
                else:
                    indices = [int(selection)]
                
                selected_services = []
                for idx in indices:
                    if 1 <= idx <= len(available_services):
                        selected_services.append(available_services[idx - 1])
                    else:
                        print(f"⚠️  Invalid selection: {idx}")
                        continue
                
                if selected_services:
                    return selected_services
                else:
                    print("⚠️  No valid services selected. Please try again.")
                    
            except ValueError:
                print("⚠️  Invalid input. Please enter numbers separated by commas or 'all'.")
    
    def _collect_service_answers(self, service_name: str, questions: List[str]) -> Dict[str, str]:
        """Collect answers for a specific service"""
        answers = {}
        
        for i, question in enumerate(questions, 1):
            print(f"\n📋 Question {i}/{len(questions)} for {service_name}:")
            print(f"   {question}")
            
            while True:
                answer = input("\n💡 Your answer: ").strip()
                if answer:
                    answers[f"q{i}"] = answer
                    break
                else:
                    print("   ⚠️  Please provide an answer.")
        
        return answers
    
    def _infer_configurations(self, service: str, answers: Dict[str, str]) -> Dict[str, str]:
        """Infer additional configurations based on user answers"""
        inferred = {}
        
        # Service-specific inference logic
        if service.upper() == 'VPC':
            inferred.update(self._infer_vpc_configs(answers))
        elif service.upper() == 'EC2':
            inferred.update(self._infer_ec2_configs(answers))
        elif service.upper() == 'RDS':
            inferred.update(self._infer_rds_configs(answers))
        elif service.upper() == 'S3':
            inferred.update(self._infer_s3_configs(answers))
        elif service.upper() == 'LAMBDA':
            inferred.update(self._infer_lambda_configs(answers))
        elif service.upper() == 'ALB':
            inferred.update(self._infer_alb_configs(answers))
        
        return inferred
    
    def _infer_vpc_configs(self, answers: Dict[str, str]) -> Dict[str, str]:
        """Infer VPC-related configurations"""
        inferred = {}
        
        # Example inference logic for VPC
        for key, value in answers.items():
            value_lower = value.lower()
            
            # Infer environment settings
            if any(env in value_lower for env in ['prod', 'production']):
                inferred['vpc_environment'] = 'production'
                inferred['vpc_enable_flow_logs'] = 'true'
            elif any(env in value_lower for env in ['dev', 'development']):
                inferred['vpc_environment'] = 'development'
                inferred['vpc_enable_flow_logs'] = 'false'
            
            # Infer CIDR requirements
            if 'large' in value_lower or 'enterprise' in value_lower:
                inferred['vpc_suggested_cidr'] = '10.0.0.0/16'
            elif 'small' in value_lower or 'startup' in value_lower:
                inferred['vpc_suggested_cidr'] = '10.0.0.0/20'
        
        return inferred
    
    def _infer_ec2_configs(self, answers: Dict[str, str]) -> Dict[str, str]:
        """Infer EC2-related configurations"""
        inferred = {}
        
        for key, value in answers.items():
            value_lower = value.lower()
            
            # Infer instance types
            if any(term in value_lower for term in ['high performance', 'compute intensive']):
                inferred['ec2_suggested_instance_type'] = 'c5.large'
            elif any(term in value_lower for term in ['web server', 'frontend', 'simple']):
                inferred['ec2_suggested_instance_type'] = 't3.micro'
            elif any(term in value_lower for term in ['database', 'memory intensive']):
                inferred['ec2_suggested_instance_type'] = 'r5.large'
            
            # Infer storage requirements
            if any(term in value_lower for term in ['high iops', 'database', 'performance']):
                inferred['ec2_suggested_storage_type'] = 'gp3'
            else:
                inferred['ec2_suggested_storage_type'] = 'gp2'
        
        return inferred
    
    def _infer_rds_configs(self, answers: Dict[str, str]) -> Dict[str, str]:
        """Infer RDS-related configurations"""
        inferred = {}
        
        for key, value in answers.items():
            value_lower = value.lower()
            
            # Infer database engine
            if 'mysql' in value_lower:
                inferred['rds_suggested_engine'] = 'mysql'
                inferred['rds_suggested_version'] = '8.0'
            elif 'postgres' in value_lower:
                inferred['rds_suggested_engine'] = 'postgres'
                inferred['rds_suggested_version'] = '14'
            
            # Infer instance class
            if any(term in value_lower for term in ['small', 'test', 'dev']):
                inferred['rds_suggested_instance_class'] = 'db.t3.micro'
            elif any(term in value_lower for term in ['production', 'large']):
                inferred['rds_suggested_instance_class'] = 'db.r5.large'
        
        return inferred
    
    def _infer_s3_configs(self, answers: Dict[str, str]) -> Dict[str, str]:
        """Infer S3-related configurations"""
        inferred = {}
        
        for key, value in answers.items():
            value_lower = value.lower()
            
            # Infer storage class
            if any(term in value_lower for term in ['archive', 'backup', 'long term']):
                inferred['s3_suggested_storage_class'] = 'GLACIER'
            elif any(term in value_lower for term in ['frequent', 'active']):
                inferred['s3_suggested_storage_class'] = 'STANDARD'
            else:
                inferred['s3_suggested_storage_class'] = 'STANDARD_IA'
            
            # Infer versioning
            if any(term in value_lower for term in ['important', 'critical', 'production']):
                inferred['s3_enable_versioning'] = 'true'
        
        return inferred
    
    def _infer_lambda_configs(self, answers: Dict[str, str]) -> Dict[str, str]:
        """Infer Lambda-related configurations"""
        inferred = {}
        
        for key, value in answers.items():
            value_lower = value.lower()
            
            # Infer runtime
            if 'python' in value_lower:
                inferred['lambda_suggested_runtime'] = 'python3.9'
            elif 'node' in value_lower or 'javascript' in value_lower:
                inferred['lambda_suggested_runtime'] = 'nodejs18.x'
            
            # Infer memory
            if any(term in value_lower for term in ['heavy', 'processing', 'compute']):
                inferred['lambda_suggested_memory'] = '1024'
            else:
                inferred['lambda_suggested_memory'] = '128'
        
        return inferred
    
    def _infer_alb_configs(self, answers: Dict[str, str]) -> Dict[str, str]:
        """Infer ALB-related configurations"""
        inferred = {}
        
        for key, value in answers.items():
            value_lower = value.lower()
            
            # Infer SSL requirements
            if any(term in value_lower for term in ['https', 'ssl', 'secure', 'production']):
                inferred['alb_enable_ssl'] = 'true'
                inferred['alb_suggested_certificate_type'] = 'ACM'
            
            # Infer internal vs internet-facing
            if any(term in value_lower for term in ['internal', 'private']):
                inferred['alb_scheme'] = 'internal'
            else:
                inferred['alb_scheme'] = 'internet-facing'
        
        return inferred
    
    def _parse_service_questions_from_file(self, file_path: str) -> Dict[str, List[str]]:
        """Parse service questions from the generated file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self._parse_service_questions(content)
    
    def _parse_questions_from_file(self, content: str) -> List[str]:
        """Parse questions from the generated file (legacy method)"""
        lines = content.split('\n')
        questions = []
        
        for line in lines:
            line = line.strip()
            # Look for numbered questions
            if line and line[0].isdigit() and '.' in line:
                # Extract question text
                question = line.split('.', 1)[1].strip()
                if question:
                    questions.append(question)
        
        return questions
    
    def get_configuration_summary(self, answers: Dict[str, str]) -> Dict[str, any]:
        """Generate a configuration summary from collected answers"""
        summary = {
            'selected_services': [],
            'configurations': {},
            'inferred_values': {},
            'terraform_variables': {}
        }
        
        # Group answers by service
        service_configs = {}
        for key, value in answers.items():
            if '_' in key:
                service = key.split('_')[0]
                if service not in service_configs:
                    service_configs[service] = {}
                service_configs[service][key] = value
        
        summary['selected_services'] = list(service_configs.keys())
        summary['configurations'] = service_configs
        
        # Extract inferred values
        for key, value in answers.items():
            if 'suggested' in key or 'enable' in key or 'environment' in key:
                summary['inferred_values'][key] = value
        
        # Map to potential Terraform variables
        summary['terraform_variables'] = self._map_to_terraform_variables(answers)
        
        return summary
    
    def _map_to_terraform_variables(self, answers: Dict[str, str]) -> Dict[str, str]:
        """Map user answers to Terraform variable names"""
        tf_vars = {}
        
        # Service enable flags
        services_mentioned = set()
        for key in answers.keys():
            service = key.split('_')[0].upper()
            if service in ['VPC', 'EC2', 'RDS', 'S3', 'LAMBDA', 'ALB', 'EKS', 'CLOUDWATCH']:
                services_mentioned.add(service.lower())
        
        # Set create flags
        for service in services_mentioned:
            tf_vars[f'create_{service}'] = 'true'
        
        # Map specific configurations
        for key, value in answers.items():
            if 'cidr' in key.lower():
                tf_vars['vpc_cidr'] = value
            elif 'instance_type' in key:
                tf_vars['instance_type'] = value
            elif 'engine' in key and 'rds' in key:
                tf_vars['db_engine'] = value
            elif 'bucket' in key.lower():
                tf_vars['s3_bucket_name'] = value
            elif 'runtime' in key and 'lambda' in key:
                tf_vars['lambda_runtime'] = value
        
        return tf_vars
    
    def print_configuration_summary(self, answers: Dict[str, str]):
        """Print a formatted summary of the configuration"""
        summary = self.get_configuration_summary(answers)
        
        print("\n" + "="*60)
        print("📋 CONFIGURATION SUMMARY")
        print("="*60)
        
        print(f"\n🎯 Selected Services: {', '.join(summary['selected_services'])}")
        
        print(f"\n🔧 Total Configurations: {len(answers)}")
        print(f"🤖 Inferred Values: {len(summary['inferred_values'])}")
        print(f"📝 Terraform Variables: {len(summary['terraform_variables'])}")
        
        if summary['inferred_values']:
            print(f"\n💡 Key Inferred Configurations:")
            for key, value in list(summary['inferred_values'].items())[:5]:
                print(f"   • {key}: {value}")
        
        print(f"\n✅ Configuration collection complete!")
        print(f"   Ready for Terraform variable generation and deployment.")
    
    def get_variable_questions(self) -> Dict[str, str]:
        """Generate specific questions for each Terraform variable"""
        variable_questions = {}
        
        for var_name, var_info in self.terraform_parser.variables.items():
            question = self._generate_variable_question(var_name, var_info)
            variable_questions[var_name] = question
        
        return variable_questions
    
    def _generate_variable_question(self, var_name: str, var_info: Dict) -> str:
        """Generate a specific question for a Terraform variable"""
        description = var_info.get('description', '')
        var_type = var_info.get('type', 'string')
        default = var_info.get('default')
        
        # Base question
        question = f"What should be the value for '{var_name}'?"
        
        # Add description if available
        if description:
            question += f" ({description})"
        
        # Add type information
        if 'bool' in var_type:
            question += " [yes/no]"
        elif default is not None:
            question += f" [default: {default}]"
        
        return question
