"""
Test client for Terraform Bot API
Demonstrates how to use the API endpoints
"""
import requests
import json

class TerraformBotAPIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def get_services(self):
        """Get available AWS services"""
        response = requests.get(f"{self.base_url}/services")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting services: {response.status_code} - {response.text}")
            return None
    
    def get_questions(self, services):
        """Get questions for selected services"""
        payload = {"services": services}
        response = requests.post(
            f"{self.base_url}/questions",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error getting questions: {response.status_code} - {response.text}")
            return None
    
    def generate_terraform(self, qa_pairs, output_file="terraform.tfvars"):
        """Generate Terraform vars file from Q&A pairs"""
        payload = {"qa_pairs": qa_pairs}
        response = requests.post(
            f"{self.base_url}/generate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"✅ Terraform file generated: {output_file}")
            return True
        else:
            print(f"Error generating terraform: {response.status_code} - {response.text}")
            return False
    
    def health_check(self):
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error checking health: {response.status_code} - {response.text}")
            return None

def demo_workflow():
    """Demonstrate the complete API workflow"""
    print("🚀 Terraform Bot API Demo")
    print("=" * 50)
    
    client = TerraformBotAPIClient()
    
    # 1. Health check
    print("\n1. Checking API health...")
    health = client.health_check()
    if health:
        print(f"✅ API Status: {health['status']}")
        print(f"📄 Message: {health['message']}")
    else:
        print("❌ API is not responding. Make sure the server is running.")
        return
    
    # 2. Get available services
    print("\n2. Getting available AWS services...")
    services = client.get_services()
    if services:
        print(f"✅ Found {len(services)} AWS services:")
        for service in services:
            print(f"   • {service['name']}: {service['description']}")
    else:
        print("❌ No services found.")
        return
    
    # 3. Select services and get questions
    print("\n3. Getting questions for VPC and EC2...")
    selected_services = ["VPC", "EC2"]
    questions = client.get_questions(selected_services)
    if questions:
        print("✅ Questions retrieved:")
        for service_q in questions:
            print(f"\n   📋 {service_q['service']} Questions:")
            for i, question in enumerate(service_q['questions'], 1):
                print(f"      {i}. {question}")
    else:
        print("❌ No questions found.")
        return
    
    # 4. Create sample answers and generate Terraform
    print("\n4. Generating Terraform file with sample answers...")
    sample_qa_pairs = [
        {"question": "What is your project name?", "answer": "my-demo-app"},
        {"question": "What AWS region do you want to deploy to?", "answer": "us-east-1"},
        {"question": "What CIDR block would you like for your VPC?", "answer": "10.0.0.0/16"},
        {"question": "How many availability zones do you want to use?", "answer": "2"},
        {"question": "What instance type do you need?", "answer": "t3.medium"},
        {"question": "How many instances do you want to launch initially?", "answer": "2"}
    ]
    
    success = client.generate_terraform(sample_qa_pairs, "demo_terraform.tfvars")
    if success:
        print("✅ Demo completed successfully!")
        print("📁 Check the generated 'demo_terraform.tfvars' file")
    else:
        print("❌ Demo failed.")

def interactive_demo():
    """Interactive demo where user can input their own answers"""
    print("🎯 Interactive Terraform Bot API Demo")
    print("=" * 50)
    
    client = TerraformBotAPIClient()
    
    # Health check
    health = client.health_check()
    if not health or health['status'] != 'healthy':
        print("❌ API is not healthy. Please check the server.")
        return
    
    # Get services
    services = client.get_services()
    if not services:
        print("❌ No services available.")
        return
    
    print(f"\n📋 Available AWS Services:")
    for i, service in enumerate(services, 1):
        print(f"   {i}. {service['name']}")
    
    # Let user select services
    while True:
        try:
            selection = input("\nEnter service numbers (comma-separated, e.g., 1,2): ").strip()
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            selected_services = [services[i]['name'] for i in indices if 0 <= i < len(services)]
            if selected_services:
                break
            print("❌ Invalid selection. Please try again.")
        except:
            print("❌ Invalid input. Please enter numbers separated by commas.")
    
    print(f"\n✅ Selected services: {', '.join(selected_services)}")
    
    # Get questions
    questions = client.get_questions(selected_services)
    if not questions:
        print("❌ No questions found for selected services.")
        return
    
    # Collect answers
    qa_pairs = []
    print("\n🎯 Please answer the following questions:")
    for service_q in questions:
        print(f"\n📋 {service_q['service']} Configuration:")
        for question in service_q['questions']:
            answer = input(f"   {question}\n   Answer: ").strip()
            qa_pairs.append({"question": question, "answer": answer})
    
    # Generate Terraform
    print("\n🔨 Generating Terraform file...")
    success = client.generate_terraform(qa_pairs, "interactive_terraform.tfvars")
    if success:
        print("✅ Interactive demo completed!")
        print("📁 Check the generated 'interactive_terraform.tfvars' file")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_demo()
    else:
        demo_workflow()
        
        print("\n" + "=" * 50)
        print("💡 To run an interactive demo, use:")
        print("   python test_client.py --interactive")
