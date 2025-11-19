# Dev-QA: S3 File Synchronization System (DEV Environment)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-Active-brightgreen.svg)](https://github.com/najam009/Dev-QA/actions)

## � Development Branch

> **⚠️ NOTICE**: You are on the **DEV** branch. This branch has **active CI/CD** pipelines and is intended for development and testing purposes.

## �📋 Table of Contents
- [Overview](#overview)
- [Dev Environment Features](#dev-environment-features)
- [CI/CD Pipeline](#cicd-pipeline)
- [Quick Start](#quick-start)
- [Development Workflow](#development-workflow)
- [Docker Configuration](#docker-configuration)
- [Environment Setup](#environment-setup)
- [Testing](#testing)
- [Deployment Process](#deployment-process)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🎯 Overview

This is the **development branch** of the Dev-QA S3 synchronization system. All new features and changes should be developed and tested here before being promoted to QA and production.

### Branch Purpose
- **Active Development**: All new features start here
- **Automated Testing**: CI/CD pipeline runs on every push
- **Docker Deployment**: Automatically builds and deploys to dev EC2 instance
- **Continuous Integration**: GitHub Actions workflow validates all changes

## ✨ Dev Environment Features

### Automated CI/CD Pipeline
- ✅ Automated Docker image building
- ✅ Push to Amazon ECR (Elastic Container Registry)
- ✅ Automated deployment to dev EC2 instance
- ✅ Container name: `myapp-dev`
- ✅ Uses `latest` image tag for development

### Key Differences from Main Branch
| Feature | Main Branch | Dev Branch |
|---------|------------|------------|
| CI/CD | ❌ None | ✅ Automated |
| Docker | Manual | Automated Build & Deploy |
| Workflow | `.github/workflows/` | ✅ `dev.yml` |
| Container Name | N/A | `myapp-dev` |
| EC2 Deployment | Manual | Automated |

## 🚀 CI/CD Pipeline

### Workflow Trigger
The CI/CD pipeline automatically runs on:
```yaml
on:
  push:
    branches:
      - dev
```

### Pipeline Stages

#### 1. Build and Push (Job 1)
```
┌─────────────────┐
│ Checkout Code   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Login to ECR    │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Build Docker    │
│ Image           │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Tag & Push to   │
│ ECR (latest)    │
└─────────────────┘
```

**Actions Performed:**
- Checkout repository code
- Login to Amazon ECR
- Build Docker image
- Tag as `latest`
- Push to ECR repository

#### 2. Deploy to EC2 (Job 2)
```
┌─────────────────┐
│ SSH to EC2      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Pull Latest     │
│ Image from ECR  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Stop & Remove   │
│ Old Container   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Run New         │
│ Container       │
│ (myapp-dev)     │
└─────────────────┘
```

**Actions Performed:**
- SSH into dev EC2 instance
- Login to ECR
- Pull latest Docker image
- Stop and remove existing `myapp-dev` container
- Start new container with updated image
- Mount volume: `/home/najam/S3bucket`
- Apply environment variables from GitHub Secrets

## 🏁 Quick Start

### Prerequisites
- AWS CLI configured
- Docker installed (for local testing)
- Access to GitHub repository
- AWS ECR repository created
- EC2 instance set up

### Local Development Setup

1. **Clone the Dev Branch**
```bash
git clone -b dev https://github.com/najam009/Dev-QA.git
cd Dev-QA
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set Up Environment**
Create `.env` file:
```env
BUCKET_NAME=your-dev-bucket
AWS_REGION=ap-south-1
HOST=your-dev-db-host
DBNAME=dev_db
USERR=dev_user
PASSWORD=dev_password
PORT=5432
```

4. **Run Locally**
```bash
python s3_database.py
```

## 👨‍💻 Development Workflow

### Making Changes

1. **Create Feature Branch** (from dev)
```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature-name
```

2. **Make Your Changes**
```bash
# Edit files
# Test locally
```

3. **Test Locally with Docker**
```bash
docker build -t dev-qa-test .
docker run -d --name test-container \
  --env-file .env \
  -v /path/to/folder:/home/najam/S3bucket \
  dev-qa-test
```

4. **Commit and Push**
```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature-name
```

5. **Create Pull Request**
- Open PR to merge into `dev` branch
- Wait for code review
- Merge when approved

6. **Automatic Deployment**
- Once merged to `dev`, CI/CD pipeline triggers automatically
- Monitor deployment in GitHub Actions tab

### Testing Your Changes

After pushing to dev branch:

1. **Monitor GitHub Actions**
   - Go to `Actions` tab in GitHub
   - Watch the CI/CD pipeline execution

2. **Verify EC2 Deployment**
```bash
ssh ec2-user@your-ec2-host
sudo docker ps | grep myapp-dev
sudo docker logs myapp-dev
```

## � Docker Configuration

### Dockerfile Details
```dockerfile
FROM python:3.10-slim
WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ARG APP_PORT=3000
ENV APP_PORT=$APP_PORT
EXPOSE $APP_PORT
CMD ["python", "s3_database.py"]
```

### Container Specifications
- **Base Image**: `python:3.10-slim`
- **Working Directory**: `/`
- **Default Port**: `3000` (configurable)
- **Entry Point**: `s3_database.py`
- **Container Name**: `myapp-dev`
- **Network Mode**: Host network

### Volume Mounts
```bash
/home/najam/S3bucket:/home/najam/S3bucket
```

## ⚙️ Environment Setup

### Required GitHub Secrets

Configure these in `Settings > Secrets and variables > Actions`:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `AWS_REGION` | AWS region | `ap-south-1` |
| `AWS_ACCOUNT_ID` | AWS account ID | `123456789012` |
| `AWS_ACCESS_KEY_ID` | AWS access key | `AKIAIOSFODNN7EXAMPLE` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `wJalrXUtnFEMI/K7MDENG/...` |
| `ECR_REPOSITORY` | ECR repository name | `dev-qa-app` |
| `EC2_HOST` | EC2 instance IP/hostname | `ec2-xx-xx-xx-xx.compute.amazonaws.com` |
| `EC2_USER` | SSH username | `ubuntu` or `ec2-user` |
| `EC2_KEY` | Private SSH key | `-----BEGIN RSA PRIVATE KEY-----...` |
| `ENV` | Environment variables file | Multi-line .env content |

### Environment Variables Structure
The `ENV` secret should contain:
```
BUCKET_NAME=dev-bucket
AWS_REGION=ap-south-1
HOST=dev-db-host.rds.amazonaws.com
DBNAME=devdb
USERR=devuser
PASSWORD=devpassword
PORT=5432
```

## 🧪 Testing

### Manual Testing Checklist
- [ ] File creation triggers S3 upload
- [ ] File modification updates S3
- [ ] File deletion removes from S3
- [ ] Database records are created
- [ ] Database records are updated
- [ ] Database records are deleted
- [ ] Folder creation works
- [ ] Folder deletion works

### Integration Testing
```bash
# Create test file
echo "test content" > /path/to/watched/folder/test.txt

# Check S3
aws s3 ls s3://your-bucket/test.txt

# Check database
psql -h localhost -U your_user -d your_db -c "SELECT * FROM s3_links WHERE file_name='test.txt';"
```

## 📦 Deployment Process

### Automated Deployment Steps

1. **Push to Dev Branch**
```bash
git push origin dev
```

2. **GitHub Actions Workflow Triggers**
   - Automatically starts CI/CD pipeline

3. **Build Phase**
   - Builds Docker image
   - Tags as `latest`
   - Pushes to Amazon ECR

4. **Deploy Phase**
   - SSHs to EC2 instance
   - Pulls new image
   - Stops old container (`myapp-dev`)
   - Starts new container with latest code

5. **Verification**
```bash
# Check running containers
sudo docker ps | grep myapp-dev

# View logs
sudo docker logs -f myapp-dev
```

### Manual Deployment (Emergency)

If automatic deployment fails:

```bash
# SSH to EC2
ssh your-ec2-host

# Login to ECR
aws ecr get-login-password --region ap-south-1 | \
  sudo docker login --username AWS --password-stdin \
  YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com

# Pull latest image
sudo docker pull YOUR_ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/ECR_REPO:latest

# Stop old container
sudo docker stop myapp-dev
sudo docker rm myapp-dev

# Run new container
sudo docker run -d \
  --name myapp-dev \
  --network host \
  --env-file /path/to/.env \
  -v /home/najam/S3bucket:/home/najam/S3bucket \
  YOUR_ECR_IMAGE:latest
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. **CI/CD Pipeline Fails**
```
Error: Unable to locate credentials
```
**Solution**: Check GitHub Secrets are correctly configured

#### 2. **Docker Build Fails**
```
Error: failed to solve with frontend dockerfile.v0
```
**Solution**: Check Dockerfile syntax and dependencies

#### 3. **ECR Push Access Denied**
```
Error: denied: User is not authorized
```
**Solution**: Verify IAM permissions for ECR push

#### 4. **SSH Connection Failed**
```
Error: Permission denied (publickey)
```
**Solution**: Verify EC2_KEY secret contains valid private key

#### 5. **Container Won't Start**
```
Container exits immediately
```
**Solution**: Check container logs
```bash
sudo docker logs myapp-dev
```

### Debug Mode

Enable verbose logging in workflow:
```yaml
- name: Debug Info
  run: |
    echo "Branch: ${{ github.ref }}"
    echo "Commit: ${{ github.sha }}"
    docker images
```

### Monitoring Commands

```bash
# Watch CI/CD progress
watch -n 2 'sudo docker ps | grep myapp-dev'

# Monitor logs in real-time
sudo docker logs -f myapp-dev

# Check resource usage
sudo docker stats myapp-dev

# Inspect container
sudo docker inspect myapp-dev
```

## 🤝 Contributing

### Development Guidelines

1. **Code Standards**
   - Follow PEP 8 for Python code
   - Add docstrings to all functions
   - Use meaningful variable names

2. **Commit Messages**
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `refactor:` Code refactoring
   - `test:` Adding tests

3. **Pull Request Process**
   - Create PR to `dev` branch
   - Describe changes clearly
   - Link related issues
   - Wait for CI/CD to pass
   - Request review from maintainers

### Branch Promotion
```
dev → qa → main
```

When features are stable:
1. Merge `dev` → `qa` for QA testing
2. After QA approval, merge `qa` → `main`

## � Monitoring & Logs

### View Application Logs
```bash
# Last 100 lines
sudo docker logs --tail 100 myapp-dev

# Follow live logs
sudo docker logs -f myapp-dev

# Logs with timestamps
sudo docker logs -t myapp-dev
```

### GitHub Actions Logs
- Navigate to `Actions` tab
- Click on workflow run
- View detailed logs for each step

## � Additional Resources

- [Main Branch Documentation](../main/README.md)
- [QA Branch Documentation](../qa/README.md)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## 🔄 Related Branches

- **main**: Production-ready stable branch
- **qa**: Quality assurance and testing branch
- **dev**: Active development branch (you are here)

---

**Development Team**: [@najam009](https://github.com/najam009)

**Last Updated**: Check git commit history

**CI/CD Status**: [![CI/CD](https://github.com/najam009/Dev-QA/actions/workflows/dev.yml/badge.svg)](https://github.com/najam009/Dev-QA/actions/workflows/dev.yml)
