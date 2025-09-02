# Terraform Bot API - Makefile
# Cross-platform commands for development and deployment

.PHONY: help install dev run build docker-build docker-run k8s-deploy k8s-clean test clean

# Variables
IMAGE_NAME := terraform-bot-api
IMAGE_TAG := latest
CONTAINER_NAME := terraform-bot-api-container
K8S_NAMESPACE := default

help: ## Show this help message
	@echo "Terraform Bot API - Available Commands"
	@echo "======================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest httpx

run: ## Run the API locally
	@echo "Starting Terraform Bot API..."
	cd api && python start_api.py

run-direct: ## Run the API directly with uvicorn
	uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run: ## Run the API in Docker container
	@echo "Running Docker container..."
	docker run -d \
		--name $(CONTAINER_NAME) \
		-p 8000:8000 \
		-e OPENAI_API_KEY=$(OPENAI_API_KEY) \
		$(IMAGE_NAME):$(IMAGE_TAG)

docker-stop: ## Stop Docker container
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

docker-logs: ## Show Docker container logs
	docker logs -f $(CONTAINER_NAME)

compose-up: ## Start with Docker Compose
	docker-compose up -d

compose-down: ## Stop Docker Compose
	docker-compose down

k8s-deploy: ## Deploy to Kubernetes
	@echo "Deploying to Kubernetes..."
	cd k8s && chmod +x deploy.sh && ./deploy.sh --build

k8s-deploy-only: ## Deploy to Kubernetes without building
	@echo "Deploying to Kubernetes (no build)..."
	cd k8s && chmod +x deploy.sh && ./deploy.sh

k8s-clean: ## Clean Kubernetes deployment
	kubectl delete -f k8s/deployment.yaml -n $(K8S_NAMESPACE) || true
	kubectl delete -f k8s/configmap-templates.yaml -n $(K8S_NAMESPACE) || true

k8s-status: ## Show Kubernetes deployment status
	kubectl get pods,svc,ingress -l app=terraform-bot-api -n $(K8S_NAMESPACE)

k8s-logs: ## Show Kubernetes pod logs
	kubectl logs -l app=terraform-bot-api -n $(K8S_NAMESPACE) --tail=100 -f

k8s-port-forward: ## Port forward Kubernetes service
	kubectl port-forward svc/terraform-bot-api-service 8000:80 -n $(K8S_NAMESPACE)

test: ## Run tests
	@echo "Running tests..."
	cd api && python test_client.py

test-interactive: ## Run interactive tests
	cd api && python test_client.py --interactive

health-check: ## Check API health
	curl -f http://localhost:8000/health || echo "API not responding"

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	rm -rf output/
	rm -rf generated_*

format: ## Format Python code
	black api/ --line-length 88
	isort api/

lint: ## Lint Python code
	flake8 api/ --max-line-length=88
	pylint api/

# Development shortcuts
dev-setup: install ## Setup development environment
	@echo "Development environment setup complete"

dev-run: run ## Alias for run

# Docker shortcuts
docker: build docker-run ## Build and run Docker container

# Kubernetes shortcuts
k8s: k8s-deploy ## Deploy to Kubernetes with build

# Show current status
status: ## Show current API status
	@echo "Checking API status..."
	@curl -s http://localhost:8000/health | jq . || echo "API not responding"
	@echo ""
	@echo "Docker containers:"
	@docker ps | grep terraform-bot || echo "No Docker containers running"
	@echo ""
	@echo "Kubernetes pods:"
	@kubectl get pods -l app=terraform-bot-api -n $(K8S_NAMESPACE) 2>/dev/null || echo "No Kubernetes pods found"
