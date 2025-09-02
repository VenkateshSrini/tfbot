#!/bin/bash

# Terraform Bot API - Kubernetes Deployment Script

set -e

# Configuration
NAMESPACE="default"
IMAGE_NAME="terraform-bot-api"
IMAGE_TAG="latest"

echo "🚀 Deploying Terraform Bot API to Kubernetes"
echo "=============================================="

# Function to check if kubectl is available
check_kubectl() {
    if ! command -v kubectl &> /dev/null; then
        echo "❌ kubectl is not installed or not in PATH"
        exit 1
    fi
    echo "✅ kubectl is available"
}

# Function to check if we can connect to Kubernetes cluster
check_cluster() {
    if ! kubectl cluster-info &> /dev/null; then
        echo "❌ Cannot connect to Kubernetes cluster"
        echo "   Please ensure kubectl is configured correctly"
        exit 1
    fi
    echo "✅ Connected to Kubernetes cluster"
}

# Function to build Docker image
build_image() {
    echo "🔨 Building Docker image..."
    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
    if [ $? -eq 0 ]; then
        echo "✅ Docker image built successfully"
    else
        echo "❌ Failed to build Docker image"
        exit 1
    fi
}

# Function to create namespace if it doesn't exist
create_namespace() {
    if kubectl get namespace ${NAMESPACE} &> /dev/null; then
        echo "✅ Namespace '${NAMESPACE}' already exists"
    else
        echo "📦 Creating namespace '${NAMESPACE}'"
        kubectl create namespace ${NAMESPACE}
    fi
}

# Function to apply Kubernetes manifests
deploy_to_k8s() {
    echo "📋 Applying Kubernetes manifests..."
    
    # Apply ConfigMap for templates first
    kubectl apply -f k8s/configmap-templates.yaml -n ${NAMESPACE}
    
    # Apply main deployment
    kubectl apply -f k8s/deployment.yaml -n ${NAMESPACE}
    
    echo "✅ Kubernetes manifests applied"
}

# Function to wait for deployment to be ready
wait_for_deployment() {
    echo "⏳ Waiting for deployment to be ready..."
    kubectl rollout status deployment/terraform-bot-api -n ${NAMESPACE} --timeout=300s
    if [ $? -eq 0 ]; then
        echo "✅ Deployment is ready"
    else
        echo "❌ Deployment failed or timed out"
        exit 1
    fi
}

# Function to show deployment status
show_status() {
    echo ""
    echo "📊 Deployment Status"
    echo "==================="
    kubectl get pods -l app=terraform-bot-api -n ${NAMESPACE}
    kubectl get services -l app=terraform-bot-api -n ${NAMESPACE}
    
    # Get service endpoint
    echo ""
    echo "🌐 Service Information"
    echo "====================="
    echo "Service Name: terraform-bot-api-service"
    echo "Namespace: ${NAMESPACE}"
    echo ""
    echo "To access the API:"
    echo "1. Port forward: kubectl port-forward svc/terraform-bot-api-service 8000:80 -n ${NAMESPACE}"
    echo "2. Then visit: http://localhost:8000/docs"
    echo ""
    echo "Or if using Ingress:"
    echo "Add '127.0.0.1 terraform-bot-api.local' to your /etc/hosts file"
    echo "Then visit: http://terraform-bot-api.local"
}

# Function to setup OpenAI API key
setup_openai_key() {
    echo ""
    echo "🔑 OpenAI API Key Setup"
    echo "======================="
    echo "You need to update the OpenAI API key in the secret."
    echo ""
    echo "1. Encode your API key:"
    echo "   echo -n 'your-actual-api-key' | base64"
    echo ""
    echo "2. Edit the secret:"
    echo "   kubectl edit secret terraform-bot-secrets -n ${NAMESPACE}"
    echo ""
    echo "3. Replace 'your-base64-encoded-openai-api-key' with your encoded key"
    echo ""
    echo "4. Restart the deployment:"
    echo "   kubectl rollout restart deployment/terraform-bot-api -n ${NAMESPACE}"
}

# Main execution
main() {
    check_kubectl
    check_cluster
    
    # Build image if requested
    if [ "$1" = "--build" ]; then
        build_image
    fi
    
    create_namespace
    deploy_to_k8s
    wait_for_deployment
    show_status
    setup_openai_key
    
    echo ""
    echo "🎉 Deployment completed successfully!"
}

# Help function
show_help() {
    echo "Terraform Bot API - Kubernetes Deployment"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --build     Build Docker image before deploying"
    echo "  --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              Deploy using existing image"
    echo "  $0 --build      Build image and deploy"
}

# Parse arguments
case "$1" in
    --help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
