# Terraform Bot API - Container & Kubernetes Deployment

This document provides detailed instructions for deploying the Terraform Bot API in containerized environments.

## Quick Start

### Docker
```bash
# Build and run
make docker

# Or manually
docker build -t terraform-bot-api .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key terraform-bot-api
```

### Kubernetes
```bash
# Deploy with automated script
make k8s

# Or manually
cd k8s && ./deploy.sh --build
```

## Docker Deployment

### Building the Image

```bash
# Build locally
docker build -t terraform-bot-api:latest .

# Build with custom tag
docker build -t your-registry/terraform-bot-api:v1.0.0 .
```

### Running the Container

**Basic run:**
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-openai-api-key \
  terraform-bot-api:latest
```

**With volume mounts:**
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-openai-api-key \
  -v $(pwd)/sample_tf:/app/sample_tf:ro \
  -v $(pwd)/output:/app/output \
  terraform-bot-api:latest
```

**Using Docker Compose:**
```bash
# Create .env file
echo "OPENAI_API_KEY=your-key" > .env

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (1.19+)
- kubectl configured
- Docker for building images
- At least 1GB RAM and 1 CPU core available

### Automated Deployment

Use the provided deployment script:

```bash
cd k8s

# Make script executable (Linux/macOS)
chmod +x deploy.sh

# Deploy with image build
./deploy.sh --build

# Deploy without building (use existing image)
./deploy.sh
```

### Manual Deployment

1. **Update the OpenAI API Key:**
   ```bash
   # Encode your API key
   echo -n 'your-actual-openai-api-key' | base64
   
   # Edit the secret in deployment.yaml
   # Replace 'your-base64-encoded-openai-api-key' with your encoded key
   ```

2. **Update Terraform Templates (Optional):**
   ```bash
   # Edit k8s/configmap-templates.yaml
   # Add your actual Terraform template content
   ```

3. **Apply Manifests:**
   ```bash
   kubectl apply -f k8s/configmap-templates.yaml
   kubectl apply -f k8s/deployment.yaml
   ```

4. **Verify Deployment:**
   ```bash
   kubectl get pods -l app=terraform-bot-api
   kubectl get services -l app=terraform-bot-api
   ```

5. **Access the API:**
   ```bash
   # Port forward
   kubectl port-forward svc/terraform-bot-api-service 8000:80
   
   # Visit http://localhost:8000/docs
   ```

### Kubernetes Features

**Deployment Configuration:**
- 2 replicas for high availability
- Resource limits (512Mi RAM, 500m CPU)
- Health checks (liveness and readiness probes)
- Security context (non-root user)

**Service Configuration:**
- ClusterIP service for internal access
- Port 80 mapping to container port 8000

**Ingress Configuration:**
- Nginx ingress controller support
- Host: terraform-bot-api.local
- HTTP redirect disabled for development

**ConfigMap & Secrets:**
- Environment variables in ConfigMap
- OpenAI API key in Secret
- Terraform templates in ConfigMap

### Production Recommendations

#### Security
```yaml
# Use non-root user (already configured)
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  
# Use secrets for sensitive data
env:
- name: OPENAI_API_KEY
  valueFrom:
    secretKeyRef:
      name: terraform-bot-secrets
      key: OPENAI_API_KEY
```

#### Resource Management
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

#### High Availability
```yaml
# Increase replicas
replicas: 3

# Add pod anti-affinity
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app
            operator: In
            values:
            - terraform-bot-api
        topologyKey: kubernetes.io/hostname
```

#### Monitoring
```yaml
# Add monitoring annotations
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| OPENAI_API_KEY | OpenAI API key | - | Yes |
| PYTHONPATH | Python path | /app | No |
| PYTHONUNBUFFERED | Unbuffered Python output | 1 | No |
| FASTAPI_HOST | Host to bind | 0.0.0.0 | No |
| FASTAPI_PORT | Port to bind | 8000 | No |

## Networking

### Ports
- **8000**: HTTP API endpoint
- **80**: Service port (Kubernetes)

### Health Checks
- **Liveness**: `GET /health` (30s interval)
- **Readiness**: `GET /health` (10s interval)

### Ingress
- **Development**: terraform-bot-api.local
- **Production**: Configure your actual domain

## Troubleshooting

### Common Issues

**Pod not starting:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Image pull errors:**
```bash
# Check if image exists
docker images | grep terraform-bot-api

# Build image if missing
docker build -t terraform-bot-api:latest .
```

**API not responding:**
```bash
# Check service
kubectl get svc terraform-bot-api-service

# Port forward and test
kubectl port-forward svc/terraform-bot-api-service 8000:80
curl http://localhost:8000/health
```

**OpenAI API key issues:**
```bash
# Check secret
kubectl get secret terraform-bot-secrets -o yaml

# Update secret
kubectl create secret generic terraform-bot-secrets \
  --from-literal=OPENAI_API_KEY=your-key \
  --dry-run=client -o yaml | kubectl apply -f -
```

### Debugging Commands

```bash
# Check all resources
kubectl get all -l app=terraform-bot-api

# View pod logs
kubectl logs -l app=terraform-bot-api --tail=100

# Execute into pod
kubectl exec -it deployment/terraform-bot-api -- /bin/bash

# Check resource usage
kubectl top pods -l app=terraform-bot-api
```

## Scaling

### Horizontal Scaling
```bash
# Scale up
kubectl scale deployment terraform-bot-api --replicas=5

# Auto-scaling (requires metrics-server)
kubectl autoscale deployment terraform-bot-api \
  --cpu-percent=70 --min=2 --max=10
```

### Vertical Scaling
```yaml
# Update resource limits in deployment.yaml
resources:
  limits:
    memory: "1Gi"
    cpu: "1000m"
```

## Backup and Recovery

### Backup
- Terraform templates (stored in ConfigMap)
- Generated files (use persistent volumes if needed)
- Configuration and secrets

### Recovery
- Redeploy using the same manifests
- Restore secrets and ConfigMaps
- Verify health checks pass

## Monitoring and Logging

### Logs
```bash
# View real-time logs
kubectl logs -f -l app=terraform-bot-api

# Export logs
kubectl logs -l app=terraform-bot-api > api-logs.txt
```

### Metrics
- Health endpoint: `/health`
- API documentation: `/docs`
- OpenAPI spec: `/openapi.json`

For production, consider integrating with:
- Prometheus for metrics
- Grafana for dashboards  
- ELK stack for log aggregation
- Jaeger for distributed tracing
