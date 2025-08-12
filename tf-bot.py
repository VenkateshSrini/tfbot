"""
Terraform Bot - Main application entry point
AWS Infrastructure Deployment Automation Tool
Dependencies: pip install langchain langchain_community openai
"""
import os
from config import TEMPLATE_DIR, GENERATED_QUESTIONS_FILE
from terraform_parser import TerraformTemplateParser
from llm_manager import LLMManager
from terraform_question_manager import TerraformQuestionManager
from terraform_generator import TerraformGenerator

def main():
    """Main application flow for Terraform Bot"""
    print("🚀 Welcome to Terraform Bot - AWS Infrastructure Automation!")
    print("=" * 60)
    
    # Initialize components
    print("⚙️  Initializing Terraform Bot components...")
    parser = TerraformTemplateParser()
    llm_manager = LLMManager()
    question_manager = TerraformQuestionManager(llm_manager, parser)
    terraform_generator = TerraformGenerator(llm_manager)
    
    try:
        # Ensure questions exist (will generate if missing)
        print("\n📋 Preparing infrastructure questions...")
        gen_q_path = question_manager.ensure_questions_exist()
        
        # Collect answers from user
        print("\n🎯 Collecting your AWS infrastructure requirements...")
        answers = question_manager.collect_answers(gen_q_path)
        
        if not answers:
            print("❌ No answers collected. Exiting.")
            return
        
        # Show configuration summary
        question_manager.print_configuration_summary(answers)
        
        # Generate Terraform variables file
        print("\n🔨 Generating Terraform configuration...")
        terraform_file = terraform_generator.generate_terraform_vars_gpt4(answers, parser)
        # Ask user for generation method
        # print("\nChoose generation method:")
        # print("1. AI-powered (GPT-4.1) - Recommended")
        # print("2. Rule-based - Fast")
        
        # while True:
        #     choice = input("\nEnter your choice (1 or 2): ").strip()
        #     if choice in ['1', '2']:
        #         break
        #     print("⚠️  Please enter 1 or 2")
        
        # if choice == '1':
        #     terraform_file = terraform_generator.generate_terraform_vars_gpt4(answers, parser)
        # else:
        #     terraform_file = terraform_generator.generate_terraform_vars_manual(answers, parser)
        
        # Validate generated file
        if terraform_generator.validate_generated_file():
            print(f"\n✅ SUCCESS! Your AWS infrastructure configuration is ready!")
            print(f"📁 Generated file: {terraform_file}")
            print("\n🚀 Next steps:")
            print("   1. Review the generated terraform.tfvars file")
            print("   2. Run 'terraform init' to initialize")
            print("   3. Run 'terraform plan' to preview changes")
            print("   4. Run 'terraform apply' to deploy to AWS")
            print("\n⚠️  Important: Ensure your AWS credentials are configured!")
        else:
            print("❌ Error: Generated file validation failed.")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your configuration and try again.")

def show_template_info():
    """Show information about the current Terraform template"""
    parser = TerraformTemplateParser()
    analysis = parser.analyze_template()
    
    print("\n📊 TERRAFORM TEMPLATE ANALYSIS")
    print("=" * 50)
    print(f"Variables: {analysis['total_variables']}")
    print(f"Resources: {analysis['total_resources']}")
    
    if analysis['categories']:
        print("\n📋 Variable Categories:")
        for category, variables in analysis['categories'].items():
            print(f"  {category}: {len(variables)} variables")
    
    if analysis['conditional']:
        print("\n🔧 Available AWS Services:")
        for service in analysis['conditional'].keys():
            print(f"  • {service.upper()}")
    
    aws_services = set(r['aws_service'] for r in analysis['resources'].values())
    print(f"\n☁️  AWS Services: {', '.join(sorted(aws_services))}")

if __name__ == "__main__":
    import sys
    
    # Check for info flag
    if len(sys.argv) > 1 and sys.argv[1] in ['--info', '-i']:
        show_template_info()
    else:
        main()
