# Dev-QA: S3 File Synchronization System (QA Environment)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)
[![QA Testing](https://img.shields.io/badge/QA-Active-blue.svg)](https://github.com/najam009/Dev-QA/actions)

## 🧪 Quality Assurance Branch

> **⚠️ NOTICE**: You are on the **QA** branch. This branch has **active CI/CD** pipelines and is intended for quality assurance and user acceptance testing (UAT).

## 📋 Table of Contents
- [Overview](#overview)
- [QA Environment Overview](#qa-environment-overview)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing Requirements](#testing-requirements)
- [QA Workflow](#qa-workflow)
- [Environment Configuration](#environment-configuration)
- [Test Scenarios](#test-scenarios)
- [Deployment Process](#deployment-process)
- [Bug Reporting](#bug-reporting)
- [Promotion to Production](#promotion-to-production)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This is the **QA (Quality Assurance)** branch of the Dev-QA S3 synchronization system. Code that passes development testing is promoted here for comprehensive QA testing before production deployment.

### Branch Purpose
- **Quality Assurance Testing**: Comprehensive testing of features from dev
- **User Acceptance Testing (UAT)**: Validation by stakeholders
- **Automated Deployment**: CI/CD pipeline deploys to QA EC2 instance
- **Pre-Production Validation**: Final testing before main/production

## ✨ QA Environment Features

### Automated CI/CD Pipeline
- ✅ Automated Docker image building with QA tag
- ✅ Push to Amazon ECR with `qa1` tag
- ✅ Automated deployment to QA EC2 instance
- ✅ Container name: `myapp-qa`
- ✅ Separate environment variables (VEN secret)

### Key Differences from Other Branches

| Feature | Dev Branch | QA Branch | Main Branch |
|---------|------------|-----------|-------------|
| Purpose | Development | Testing | Production |
| CI/CD | ✅ Automated | ✅ Automated | ❌ Manual |
| Docker Tag | `latest` | `qa1` | N/A |
| Container Name | `myapp-dev` | `myapp-qa` | N/A |
| Env Secret | `ENV` | `VEN` | N/A |
| Stability | Low | Medium | High |
| Testing | Developer | QA Team | End Users |

## 🚀 CI/CD Pipeline

### Workflow Trigger
The CI/CD pipeline automatically runs when code is pushed to QA:
```yaml
on:
  push:
    branches:
      - qa
```

### Pipeline Architecture

```
┌──────────────────┐
│  Code Push to    │
│  QA Branch       │
└────────┬─────────┘
         ▼
┌────────────────────────────┐
│  Job 1: Build & Push       │
├────────────────────────────┤
│  1. Checkout Code          │
│  2. Login to ECR           │
│  3. Build Docker Image     │
│  4. Tag as 'qa1'           │
│  5. Push to ECR            │
└────────┬───────────────────┘
         ▼
┌────────────────────────────┐
│  Job 2: Deploy to EC2 (QA) │
├────────────────────────────┤
│  1. SSH to QA EC2          │
│  2. Pull qa1 image         │
│  3. Stop myapp-qa          │
│  4. Remove old container   │
│  5. Run new myapp-qa       │
│  6. Apply VEN variables    │
└────────────────────────────┘
```

### Unique QA Pipeline Features

#### 1. QA-Specific Image Tag
```bash
docker build -t $ECR_REPOSITORY:qa1 .
```
- Uses `qa1` tag instead of `latest`
- Allows parallel deployment with dev
- Clear version identification

#### 2. QA Environment Variables
```yaml
echo "${{ secrets.VEN }}" > "$TEMP_ENV"
```
- Uses `VEN` secret (not `ENV`)
- Separate configuration from dev
- QA-specific database and S3 bucket

#### 3. QA Container Name
```bash
--name myapp-qa
```
- Distinct from dev container (`myapp-dev`)
- Can run simultaneously on same server
- Clear environment separation

## 🧪 Testing Requirements

### Pre-Deployment Checklist
Before promoting code to QA:
- [ ] All dev tests passing
- [ ] Code reviewed and approved
- [ ] No critical bugs in dev environment
- [ ] Feature complete and ready for testing
- [ ] Documentation updated

### QA Testing Phases

#### Phase 1: Smoke Testing (Day 1)
- [ ] Application starts successfully
- [ ] Database connection established
- [ ] S3 connection working
- [ ] Basic file operations functional

#### Phase 2: Functional Testing (Day 2-3)
- [ ] File creation and upload
- [ ] File modification and sync
- [ ] File deletion and removal
- [ ] Folder operations
- [ ] Database record management
- [ ] Error handling

#### Phase 3: Integration Testing (Day 4)
- [ ] Complete workflow testing
- [ ] Multiple file operations
- [ ] Concurrent operations
- [ ] Large file handling
- [ ] Network failure recovery

#### Phase 4: Performance Testing (Day 5)
- [ ] Load testing with multiple files
- [ ] Memory usage monitoring
- [ ] CPU utilization check
- [ ] Response time validation
- [ ] Resource leak detection

#### Phase 5: Security Testing (Day 6)
- [ ] AWS credentials security
- [ ] Database connection security
- [ ] File permission validation
- [ ] S3 bucket access control
- [ ] Environment variable protection

#### Phase 6: User Acceptance Testing (Day 7)
- [ ] Stakeholder review
- [ ] Business requirements validation
- [ ] End-user feedback
- [ ] Final approval for production

## 🔄 QA Workflow

### Standard QA Process

```
┌────────────────┐
│  Dev Branch    │  ← Features developed and tested
│  (Development) │
└───────┬────────┘
        │ Merge when ready for QA
        ▼
┌────────────────┐
│  QA Branch     │  ← Automated deployment
│  (Testing)     │
└───────┬────────┘
        │
        ▼
┌────────────────────┐
│  QA Testing        │
│  (Test all phases) │
└───────┬────────────┘
        │
        ├─ Bugs Found → Create Issues → Fix in Dev → Re-test
        │
        ▼
┌────────────────┐
│  QA Approval   │
└───────┬────────┘
        │
        ▼
┌────────────────┐
│  Main Branch   │  ← Production deployment
│  (Production)  │
└────────────────┘
```

### Merging from Dev to QA

1. **Ensure Dev is Stable**
```bash
git checkout dev
git pull origin dev
# Run all tests
```

2. **Merge to QA**
```bash
git checkout qa
git pull origin qa
git merge dev
```

3. **Resolve Conflicts** (if any)
```bash
# Resolve conflicts manually
git add .
git commit -m "merge: Merge dev into qa for testing"
```

4. **Push to QA**
```bash
git push origin qa
```

5. **Monitor Deployment**
- Check GitHub Actions
- Verify EC2 deployment
- Begin testing

## ⚙️ Environment Configuration

### QA-Specific GitHub Secrets

| Secret Name | Description | QA Value Example |
|-------------|-------------|------------------|
| `VEN` | QA environment variables | Multi-line .env for QA |
| `AWS_REGION` | AWS region | `ap-south-1` |
| `AWS_ACCOUNT_ID` | AWS account | `123456789012` |
| `ECR_REPOSITORY` | ECR repo name | `dev-qa-app` |
| `EC2_HOST` | QA EC2 host | `qa-ec2.example.com` |
| `EC2_USER` | SSH username | `ubuntu` |
| `EC2_KEY` | SSH private key | `-----BEGIN RSA...` |

### VEN Secret Structure
The `VEN` secret should contain QA-specific configuration:
```env
BUCKET_NAME=qa-testing-bucket
AWS_REGION=ap-south-1
HOST=qa-db.example.com
DBNAME=qa_database
USERR=qa_user
PASSWORD=qa_secure_password
PORT=5432
```

### Important Configuration Notes
⚠️ **Use separate resources for QA:**
- Different S3 bucket from dev
- Separate PostgreSQL database
- Isolated AWS resources
- Prevents test data pollution

## 📝 Test Scenarios

### Scenario 1: File Upload Flow
```
Action: Create new file in watched folder
Expected:
  1. File uploaded to S3 within 2 seconds
  2. Database record created
  3. S3 URL is valid and accessible
  4. File content matches original
```

### Scenario 2: File Modification
```
Action: Modify existing file
Expected:
  1. Updated file uploads to S3
  2. Database record updated with new timestamp
  3. S3 file content reflects changes
  4. No duplicate records created
```

### Scenario 3: File Deletion
```
Action: Delete file from watched folder
Expected:
  1. File removed from S3
  2. Database record deleted
  3. S3 URL returns 404
  4. No orphaned records
```

### Scenario 4: Folder Operations
```
Action: Create/delete folders
Expected:
  1. Folder placeholder (.keep) created in S3
  2. Nested structure maintained
  3. Folder deletion removes all contents
  4. No broken references
```

### Scenario 5: Error Handling
```
Action: Simulate connection failures
Test Cases:
  1. S3 unavailable → Retry mechanism works
  2. Database down → Graceful error handling
  3. Invalid credentials → Clear error message
  4. Disk full → Appropriate error log
```

### Scenario 6: Concurrent Operations
```
Action: Multiple simultaneous file changes
Expected:
  1. All files processed correctly
  2. No race conditions
  3. Database integrity maintained
  4. No data loss
```

## 📦 Deployment Process

### Automated Deployment

1. **Code Pushed to QA**
```bash
git push origin qa
```

2. **GitHub Actions Triggered**
   - Workflow: `.github/workflows/qa.yml`
   - Builds Docker image with `qa1` tag

3. **ECR Push**
```bash
Image: YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/REPO:qa1
```

4. **EC2 Deployment**
```bash
Container Name: myapp-qa
Network: host
Volume: /home/najam/S3bucket
Env File: VEN secret
```

### Verification Steps

```bash
# 1. SSH to QA EC2
ssh your-qa-ec2-host

# 2. Check container status
sudo docker ps | grep myapp-qa

# 3. View container logs
sudo docker logs myapp-qa

# 4. Verify application is running
sudo docker logs -f myapp-qa | grep "Watching"

# 5. Test file operation
echo "QA Test" > /home/najam/S3bucket/qa-test.txt
```

## 🐛 Bug Reporting

### Bug Report Template

```markdown
## Bug Report

**Environment**: QA
**Severity**: Critical / High / Medium / Low
**Date**: YYYY-MM-DD
**Tester**: Your Name

### Description
Brief description of the issue

### Steps to Reproduce
1. Step one
2. Step two
3. Step three

### Expected Behavior
What should happen

### Actual Behavior
What actually happened

### Screenshots/Logs
Attach relevant screenshots or logs

### Additional Context
Any other relevant information
```

### Bug Severity Levels

| Severity | Definition | Example | Action Required |
|----------|------------|---------|-----------------|
| **Critical** | System unusable | App crashes on startup | Immediate fix |
| **High** | Major feature broken | Files not uploading | Fix within 24h |
| **Medium** | Feature partially broken | Slow performance | Fix within week |
| **Low** | Minor issue | UI cosmetic issue | Future release |

### Bug Workflow

```
Bug Found → Create GitHub Issue → Assign to Dev → 
Fix in Dev → Merge to QA → Re-test → Verify Fix → Close Issue
```

## ✅ Promotion to Production

### Production Readiness Checklist

- [ ] All test phases completed successfully
- [ ] No critical or high severity bugs
- [ ] Stakeholder approval obtained
- [ ] Documentation updated
- [ ] Performance benchmarks met
- [ ] Security audit passed
- [ ] Backup and rollback plan ready

### Promotion Process

1. **Final QA Sign-off**
```bash
# Document test results
# Get stakeholder approval
```

2. **Merge QA to Main**
```bash
git checkout main
git pull origin main
git merge qa
git push origin main
```

3. **Create Release Tag**
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

4. **Production Deployment**
   - Follow main branch deployment procedures
   - Monitor closely post-deployment
   - Be ready to rollback if needed

### Post-Production Monitoring

```bash
# Monitor for 24-48 hours
# Check error logs
# Verify performance metrics
# Gather user feedback
```

## 🛠️ Troubleshooting

### Common QA Issues

#### 1. **Pipeline Fails to Deploy**
```
Error: Container myapp-qa already running
```
**Solution**:
```bash
ssh qa-ec2
sudo docker stop myapp-qa
sudo docker rm myapp-qa
# Re-run workflow
```

#### 2. **Wrong Environment Variables**
```
Error: Connection to database failed
```
**Solution**: Verify `VEN` secret contains QA configs, not dev

#### 3. **Image Tag Mismatch**
```
Error: Image not found
```
**Solution**: Ensure workflow uses `qa1` tag consistently

#### 4. **Container Logs Show Errors**
```bash
sudo docker logs myapp-qa
# Check for connection errors
```
**Solution**: Verify QA S3 bucket and database are accessible

### Debug Commands

```bash
# Check current deployment
sudo docker ps -a | grep myapp-qa

# View detailed logs
sudo docker logs --tail 200 myapp-qa

# Inspect container configuration  
sudo docker inspect myapp-qa

# Check environment variables
sudo docker exec myapp-qa env

# Access container shell
sudo docker exec -it myapp-qa /bin/bash

# Monitor resource usage
sudo docker stats myapp-qa
```

## 📊 QA Metrics and Reporting

### Test Coverage Metrics
- Total test cases: _____
- Passed: _____
- Failed: _____
- Blocked: _____
- Coverage: _____% 

### Defect Metrics
- Total bugs found: _____
- Critical: _____
- High: _____
- Medium: _____
- Low: _____
- Fixed: _____
- Open: _____

### Performance Metrics
- Average file upload time: _____ms
- Database query time: _____ms
- Memory usage: _____MB
- CPU usage: _____%

## 📚 Additional Resources

- [Main Branch Documentation](../main/README.md)
- [Dev Branch Documentation](../dev/README.md)
- [QA Testing Best Practices](https://www.softwaretestinghelp.com/qa-testing-best-practices/)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [Docker Testing Guide](https://docs.docker.com/language/python/run-tests/)

## 🔄 Branch Relationships

```
main (Production - Stable)
  ↑
  | Merge after QA approval
  |
qa (QA Testing - You are here)
  ↑
  | Merge when feature ready
  |
dev (Active Development)
```

## 👥 QA Team Contacts

- **QA Lead**: [Name/Email]
- **DevOps**: [Name/Email]
- **Product Owner**: [Name/Email]

## 📅 QA Schedule

- **Daily**: Smoke tests after deployments
- **Weekly**: Full regression testing
- **Bi-weekly**: Performance testing
- **Monthly**: Security audit

---

**QA Environment Owner**: [@najam009](https://github.com/najam009)

**Last QA Cycle**: Check commit history

**Current QA Status**: [![QA Pipeline](https://github.com/najam009/Dev-QA/actions/workflows/qa.yml/badge.svg)](https://github.com/najam009/Dev-QA/actions/workflows/qa.yml)

---

## 🎯 Remember

> **Quality is not an act, it is a habit.** - Aristotle

Testing in QA ensures that our users get a reliable, robust, and performant application. Take the time to test thoroughly!
