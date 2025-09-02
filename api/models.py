"""
API Models for Terraform Bot API
Pydantic models for request/response validation
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class AWSService(BaseModel):
    """AWS Service information"""
    name: str = Field(..., description="Service name (e.g., EC2, RDS, VPC)")
    description: str = Field(..., description="Service description")
    available: bool = Field(default=True, description="Whether service is available in template")

class ServiceSelection(BaseModel):
    """Request model for selecting AWS services"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "services": ["VPC", "EC2", "RDS"]
            }
        }
    )
    
    services: List[str] = Field(..., description="List of AWS service names to get questions for")

class ServiceQuestion(BaseModel):
    """Questions for a specific AWS service"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "service": "EC2",
                "questions": [
                    "What instance type do you need?",
                    "How many instances do you want to launch?",
                    "What operating system?"
                ]
            }
        }
    )
    
    service: str = Field(..., description="AWS service name")
    questions: List[str] = Field(..., description="List of questions for the service")

class QuestionAnswer(BaseModel):
    """Single question-answer pair"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "What instance type do you need?",
                "answer": "t3.medium"
            }
        }
    )
    
    question: str = Field(..., description="The question text")
    answer: str = Field(..., description="The user's answer")

class QARequest(BaseModel):
    """Request model for generating Terraform vars from Q&A pairs"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "qa_pairs": [
                    {
                        "question": "What is your project name?",
                        "answer": "my-web-app"
                    },
                    {
                        "question": "What AWS region do you want to deploy to?",
                        "answer": "us-east-1"
                    },
                    {
                        "question": "What instance type do you need?",
                        "answer": "t3.medium"
                    }
                ]
            }
        }
    )
    
    qa_pairs: List[QuestionAnswer] = Field(..., description="List of question-answer pairs")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Health status")
    message: str = Field(..., description="Health message")
    components: Dict[str, str] = Field(..., description="Component status")

class APIInfo(BaseModel):
    """API information response"""
    message: str = Field(..., description="API name")
    version: str = Field(..., description="API version")
    description: str = Field(..., description="API description")
    endpoints: Dict[str, str] = Field(..., description="Available endpoints")

class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str = Field(..., description="Error message")
