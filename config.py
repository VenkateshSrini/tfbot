"""Configuration settings for Terraform Bot"""
import os

# Get the project root directory (where this config.py file is located)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Directory paths - use absolute paths relative to project root
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, 'sample_tf')

# File names
GENERATED_QUESTIONS_FILE = 'generated_questions.txt'
TERRAFORM_VARS_FILE = 'terraform.tfvars'
GENERATED_TERRAFORM_FILE = 'generated_terraform.tfvars'

# LLM settings - Multi-provider support
# OpenAI Models (commented out)
# DEFAULT_MODEL = 'gpt-4.1'
# GPT4_MODEL = 'gpt-4.1'

# Anthropic Models (active) - using correct model name
DEFAULT_MODEL = 'claude-sonnet-4-20250514'
GPT4_MODEL = 'claude-sonnet-4-20250514'

# Temperature settings
DEFAULT_TEMPERATURE = 0.3
GPT4_TEMPERATURE = 0.3

# Provider detection - automatically determined by model name
SUPPORTED_OPENAI_MODELS = ['gpt-4.1', 'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo']
SUPPORTED_ANTHROPIC_MODELS = ['claude-sonnet-4-20250514', 'claude-3-5-sonnet-20240620', 'claude-3-sonnet-20240229', 'claude-3-haiku-20240307', 'claude-3-opus-20240229']

def get_provider_from_model(model_name):
    """Determine the provider based on model name"""
    if model_name in SUPPORTED_OPENAI_MODELS:
        return 'openai'
    elif model_name in SUPPORTED_ANTHROPIC_MODELS:
        return 'anthropic'
    else:
        # Default fallback based on naming convention
        if model_name.startswith('gpt'):
            return 'openai'
        elif model_name.startswith('claude'):
            return 'anthropic'
        else:
            raise ValueError(f"Unsupported model: {model_name}")

def get_api_key_env_var(provider):
    """Get the appropriate environment variable name for API key"""
    if provider == 'openai':
        return 'OPENAI_API_KEY'
    elif provider == 'anthropic':
        return 'ANTHROPIC_API_KEY'
    else:
        raise ValueError(f"Unsupported provider: {provider}")

# Terraform-specific settings
TF_MAIN_FILE = 'main.tf'
TF_VARIABLES_FILE = 'variables.tf'
TF_OUTPUTS_FILE = 'outputs.tf'
