"""
FastAPI Application for Terraform Bot
Exposes Terraform Bot functionality as REST API endpoints
"""
import os
import sys
from typing import List, Dict
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

# Add parent directory to Python path to import modules
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
sys.path.append(current_dir)

from terraform_parser import TerraformTemplateParser
from llm_manager import LLMManager
from terraform_question_manager import TerraformQuestionManager
from terraform_generator import TerraformGenerator

# Import API models and utilities
from models import (
    AWSService, ServiceSelection, ServiceQuestion, 
    QuestionAnswer, QARequest, HealthResponse, APIInfo
)
from utils import (
    get_service_descriptions, generate_basic_questions_for_service,
    format_qa_pairs_for_terraform_generator, extract_services_from_analysis,
    get_api_info
)

# Initialize components
parser = TerraformTemplateParser()
llm_manager = LLMManager()
question_manager = TerraformQuestionManager(llm_manager, parser)
terraform_generator = TerraformGenerator(llm_manager)

# Global variable to store analysis
template_analysis = None

def get_template_analysis():
    """Get or create template analysis"""
    global template_analysis
    if template_analysis is None:
        template_analysis = parser.analyze_template()
    return template_analysis

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting Terraform Bot API...")
    # Trigger analysis on startup
    get_template_analysis()
    print("✅ Terraform Bot API is ready!")
    print("📚 API documentation available at: http://localhost:8000/docs")
    yield
    # Shutdown
    print("⏹️  Shutting down Terraform Bot API...")

# Initialize FastAPI app
app = FastAPI(
    title="Terraform Bot API",
    description="AWS Infrastructure Deployment Automation API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.get("/", response_model=APIInfo)
async def root():
    """Root endpoint with API information"""
    return get_api_info()

@app.get("/services", response_model=List[AWSService])
async def get_aws_services():
    """
    Get the list of available AWS services from the Terraform template
    
    Returns a list of AWS services that can be configured using this API.
    Each service includes its name, description, and availability status.
    """
    try:
        analysis = get_template_analysis()
        
        if not analysis.get('resources'):
            raise HTTPException(status_code=404, detail="No AWS services found in template")
        
        # Extract unique AWS services
        aws_services = extract_services_from_analysis(analysis)
        service_descriptions = get_service_descriptions()
        
        services = []
        for service in aws_services:
            services.append(AWSService(
                name=service.upper(),
                description=service_descriptions.get(service.lower(), f"AWS {service.upper()} service"),
                available=True
            ))
        
        return services
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving AWS services: {str(e)}")

@app.post("/questions", response_model=List[ServiceQuestion])
async def get_questions_for_services(service_selection: ServiceSelection):
    """
    Get relevant questions based on selected AWS services
    
    Provide a list of AWS service names to get specific questions for each service.
    The questions help gather the necessary information to configure your infrastructure.
    """
    try:
        if not service_selection.services:
            raise HTTPException(status_code=400, detail="No services selected")
        
        analysis = get_template_analysis()
        
        # Ensure questions are generated
        questions_file = question_manager.ensure_questions_exist()
        
        # Try to load questions from file
        service_questions = {}
        try:
            service_questions = question_manager._load_service_questions_from_file()
        except:
            # If loading fails, use basic questions
            pass
        
        # Filter questions based on selected services
        filtered_questions = []
        for service in service_selection.services:
            service_lower = service.lower()
            
            if service_lower in service_questions and service_questions[service_lower]:
                # Use questions from generated file
                filtered_questions.append(ServiceQuestion(
                    service=service,
                    questions=service_questions[service_lower]
                ))
            else:
                # Use basic questions for service
                basic_questions = generate_basic_questions_for_service(service_lower)
                if basic_questions:
                    filtered_questions.append(ServiceQuestion(
                        service=service,
                        questions=basic_questions
                    ))
        
        if not filtered_questions:
            raise HTTPException(status_code=404, detail="No questions found for selected services")
        
        return filtered_questions
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating questions: {str(e)}")

@app.post("/generate")
async def generate_terraform_vars(qa_request: QARequest):
    """
    Generate Terraform variables file from question-answer pairs and return as download
    
    Provide a list of question-answer pairs to generate a Terraform variables file.
    The file will be generated using GPT-4 and returned as a downloadable file.
    """
    try:
        if not qa_request.qa_pairs:
            raise HTTPException(status_code=400, detail="No question-answer pairs provided")
        
        # Convert QA pairs to the format expected by terraform_generator
        qa_dict_list = [{"question": qa.question, "answer": qa.answer} for qa in qa_request.qa_pairs]
        answers = format_qa_pairs_for_terraform_generator(qa_dict_list)
        
        # Generate Terraform variables file using GPT-4
        terraform_file = terraform_generator.generate_terraform_vars_gpt4(answers, parser)
        
        # Validate the generated file
        if not terraform_generator.validate_generated_file():
            raise HTTPException(status_code=500, detail="Generated Terraform file validation failed")
        
        # Return the file as a download
        if os.path.exists(terraform_file):
            return FileResponse(
                path=terraform_file,
                filename="terraform.tfvars",
                media_type='application/octet-stream',
                headers={"Content-Disposition": "attachment; filename=terraform.tfvars"}
            )
        else:
            raise HTTPException(status_code=500, detail="Generated file not found")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Terraform file: {str(e)}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint
    
    Returns the health status of the API and its components.
    """
    try:
        # Test each component
        components_status = {
            "parser": "OK",
            "llm_manager": "OK", 
            "question_manager": "OK",
            "terraform_generator": "OK"
        }
        
        # Test template analysis
        analysis = get_template_analysis()
        if not analysis:
            components_status["parser"] = "ERROR"
        
        return HealthResponse(
            status="healthy" if all(status == "OK" for status in components_status.values()) else "degraded",
            message="Terraform Bot API is running",
            components=components_status
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            message=f"Error in health check: {str(e)}",
            components={"error": str(e)}
        )

if __name__ == "__main__":
    try:
        import uvicorn
        print("🚀 Starting Terraform Bot API Server...")
        print("📡 Server will be available at: http://localhost:8000")
        print("📚 API docs will be available at: http://localhost:8000/docs")
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    except ImportError:
        print("❌ uvicorn not installed. Please install with: pip install uvicorn[standard]")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
