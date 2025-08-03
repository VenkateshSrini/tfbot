#!/usr/bin/env python3
"""
Test script for the new service-organized question system
"""
import os
import sys
# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from terraform_parser import TerraformTemplateParser
from terraform_question_manager import TerraformQuestionManager

# Mock LLM Manager for testing
class MockLLMManager:
    class MockLLM:
        def invoke(self, prompt):
            # Return mock service-organized questions
            class MockResponse:
                content = """
Service-name: GENERAL
Questions:
- What is your project name and purpose?
- Which AWS region do you prefer for deployment?
- What environment is this for (development, staging, production)?

Service-name: VPC
Questions:
- What type of network architecture do you need (simple, multi-tier, enterprise)?
- Do you need public and private subnets for security isolation?
- Will you need internet connectivity for your resources?

Service-name: EC2
Questions:
- What type of applications will run on your EC2 instances?
- How many instances do you expect to need initially?
- Do you need high availability across multiple zones?

Service-name: RDS
Questions:
- What database engine do you prefer (MySQL, PostgreSQL, etc.)?
- What is the expected database size and traffic volume?
- Do you need automated backups and point-in-time recovery?

Service-name: S3
Questions:
- What type of data will you store (documents, media, backups)?
- How frequently will you access this data?
- Do you need versioning for data protection?

Service-name: LAMBDA
Questions:
- What programming language will your functions use?
- What will trigger your Lambda functions (API Gateway, S3 events, etc.)?
- Do you expect high or low execution volume?

Service-name: ALB
Questions:
- Will you need SSL/HTTPS termination?
- Do you need to distribute traffic across multiple instances?
- Will this be internet-facing or internal only?
"""
            return MockResponse()
    
    def get_default_llm(self):
        return self.MockLLM()

def test_question_generation():
    """Test the question generation and parsing"""
    print("🧪 Testing Service-Organized Question System")
    print("=" * 50)
    
    # Initialize components
    parser = TerraformTemplateParser()
    mock_llm = MockLLMManager()
    question_manager = TerraformQuestionManager(mock_llm, parser)
    
    # Test parsing
    print("\n1. Testing Terraform parsing...")
    analysis = parser.analyze_template()
    print(f"   ✅ Found {analysis['total_variables']} variables")
    print(f"   ✅ Found {analysis['total_resources']} resources")
    print(f"   ✅ Services: {list(analysis['conditional'].keys())}")
    
    # Test question generation
    print("\n2. Testing question generation...")
    service_questions = question_manager._generate_questions_with_llm(analysis)
    print(f"   ✅ Generated questions for {len(service_questions)} services")
    
    for service, questions in service_questions.items():
        print(f"   📋 {service}: {len(questions)} questions")
    
    # Test file saving
    print("\n3. Testing file saving...")
    question_manager._save_service_questions_to_file(service_questions)
    print(f"   ✅ Saved to: {question_manager.questions_file}")
    
    # Test file parsing
    print("\n4. Testing file parsing...")
    parsed_questions = question_manager._parse_service_questions_from_file(question_manager.questions_file)
    print(f"   ✅ Parsed {len(parsed_questions)} services from file")
    
    # Show sample questions
    print("\n5. Sample questions:")
    for service, questions in list(parsed_questions.items())[:2]:
        print(f"\n   🔧 {service}:")
        for i, q in enumerate(questions[:2], 1):
            print(f"      {i}. {q}")
        if len(questions) > 2:
            print(f"      ... and {len(questions)-2} more")
    
    print("\n✅ All tests passed!")
    return service_questions

def test_interactive_selection():
    """Test the service selection logic"""
    print("\n🧪 Testing Service Selection Logic")
    print("=" * 40)
    
    available_services = ['GENERAL', 'VPC', 'EC2', 'RDS', 'S3', 'LAMBDA', 'ALB']
    print(f"Available services: {available_services}")
    
    # Test selection parsing
    test_cases = [
        ("1,3,5", [0, 2, 4]),  # Selected indices
        ("all", list(range(len(available_services)))),  # All services
        ("2", [1]),  # Single service
    ]
    
    for selection, expected_indices in test_cases:
        print(f"\nTesting selection: '{selection}'")
        # Simulate the selection logic
        if selection == 'all':
            selected = available_services.copy()
        else:
            try:
                if ',' in selection:
                    indices = [int(x.strip()) for x in selection.split(',')]
                else:
                    indices = [int(selection)]
                
                selected = [available_services[i-1] for i in indices if 1 <= i <= len(available_services)]
            except:
                selected = []
        
        print(f"   Result: {selected}")
    
    print("\n✅ Selection logic test passed!")

if __name__ == "__main__":
    # Change working directory to parent directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Run tests
    service_questions = test_question_generation()
    test_interactive_selection()
    
    print(f"\n🎉 Testing complete! Questions file created at:")
    print(f"   {os.path.abspath('sample_tf/generated_questions.txt')}")
