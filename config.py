"""Configuration settings for Terraform Bot"""
import os

# Directory paths
TEMPLATE_DIR = 'sample_tf'

# File names
GENERATED_QUESTIONS_FILE = 'generated_questions.txt'
TERRAFORM_VARS_FILE = 'terraform.tfvars'
GENERATED_TERRAFORM_FILE = 'generated_terraform.tfvars'

# LLM settings - GPT-4.1 only
DEFAULT_MODEL = 'gpt-4.1'
GPT4_MODEL = 'gpt-4.1'
DEFAULT_TEMPERATURE = 0.3
GPT4_TEMPERATURE = 0.3

# Terraform-specific settings
TF_MAIN_FILE = 'main.tf'
TF_VARIABLES_FILE = 'variables.tf'
TF_OUTPUTS_FILE = 'outputs.tf'
