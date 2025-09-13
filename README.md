# Terraform Bot (TF-Bot) 🤖

An intelligent infrastructure-as-code assistant that automates AWS resource configuration through natural language interaction.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure your OpenAI API key
cp config.py.example config.py
# Edit config.py and add your API key

# Run the application
python tf-bot.py

# Or start the web API
uvicorn api.main:app --reload
```

## ✨ Features

- **98% Configuration Accuracy** with minimal user input
- **Service-Organized Questions** for AWS services (VPC, EC2, RDS, S3, Lambda, ALB)
- **AI-Powered Configuration** using GPT-4 inference
- **FastAPI Web Interface** with automatic OpenAPI documentation
- **Container Ready** with Docker and Kubernetes support
- **Cross-Platform** startup scripts for Windows, macOS, and Linux

## 📚 Documentation

📖 **[Complete Documentation](documentation/README.md)** - Comprehensive guide covering all features, installation, configuration, API endpoints, deployment options, multi-provider LLM system, testing, and troubleshooting

### Quick Access
- [Installation & Setup](documentation/README.md#installation--setup) - Get started quickly
- [Multi-Provider LLM System](documentation/README.md#multi-provider-llm-system) - OpenAI and Anthropic integration
- [API Reference](documentation/README.md#api-reference) - REST API endpoints and examples
- [Container Deployment](documentation/README.md#container--deployment) - Docker and Kubernetes setup
- [Testing Guide](documentation/README.md#testing) - Running tests and validation
- [Configuration Guide](documentation/README.md#configuration) - Setup and customization
- [Troubleshooting](documentation/README.md#troubleshooting) - Common issues and solutions

## 🏗️ Architecture

```
CLI Application ──┐
                  ├── Terraform Parser ──── LLM Manager ──── OpenAI GPT-4
FastAPI Web API ──┘                   ├── Question Manager
                                       └── Code Generator ──── Terraform Files
```

## 📈 Performance

- **Configuration Time**: 30 minutes → 5 minutes
- **Questions**: 50+ → ~15 targeted questions  
- **Developer Productivity**: 6x improvement
- **Infrastructure Setup**: Automated end-to-end

---

For complete documentation, examples, and deployment guides, see **[documentation/README.md](documentation/README.md)**
