# Dev-QA: S3 File Synchronization System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![AWS S3](https://img.shields.io/badge/AWS-S3-orange.svg)](https://aws.amazon.com/s3/)

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

**Dev-QA** is an automated file synchronization system that monitors a local directory and synchronizes file changes (create, modify, delete) with AWS S3 in real-time. It also maintains a PostgreSQL database with file metadata and S3 URLs for easy tracking and retrieval.

### Key Capabilities:
- 📁 Real-time local folder monitoring
- ☁️ Automatic S3 synchronization
- 🗃️ PostgreSQL database integration for file metadata
- 🐳 Docker containerization support
- 🔄 Bi-directional sync operations

## ✨ Features

### Core Functionality
- **Real-time File Monitoring**: Uses `watchdog` library to detect file system changes instantly
- **S3 Synchronization**: Automatically uploads, updates, and deletes files in S3
- **Database Logging**: Records all file operations in PostgreSQL with S3 URLs
- **Folder Support**: Handles folder creation and deletion with placeholder files
- **Error Handling**: Robust exception handling for network and database failures

### Available Scripts
1. **`local_watcher.py`** - Basic local folder monitoring (no S3 sync)
2. **`s3_watcher.py`** - S3 synchronization without database logging
3. **`s3_database.py`** - Full S3 sync with PostgreSQL database integration (recommended)

## 🏗️ Architecture

```
┌─────────────────┐
│  Local Folder   │
│  /S3bucket/     │
└────────┬────────┘
         │ (watchdog monitors)
         ▼
┌─────────────────────────┐
│  Python Application     │
│  - s3_database.py       │
│  - FileSystemEventHandler│
└──────┬──────────┬───────┘
       │          │
       │          │
       ▼          ▼
┌──────────┐  ┌─────────────┐
│  AWS S3  │  │ PostgreSQL  │
│  Bucket  │  │  Database   │
└──────────┘  └─────────────┘
```

### Data Flow
1. File change detected in local folder
2. Event triggers appropriate handler (create/modify/delete)
3. File uploaded/deleted from S3 bucket
4. S3 URL generated
5. Database record inserted/updated/deleted

## 📦 Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **AWS Account**: With S3 access
- **PostgreSQL**: 12 or higher
- **Docker** (optional): For containerized deployment

### AWS Requirements
- Valid AWS credentials (Access Key ID & Secret Access Key)
- S3 bucket created in your preferred region
- IAM permissions for S3 operations (`s3:PutObject`, `s3:GetObject`, `s3:DeleteObject`)

### Database Requirements
- PostgreSQL database with the following table:

```sql
CREATE TABLE s3_links (
    id SERIAL PRIMARY KEY,
    file_name VARCHAR(255) UNIQUE NOT NULL,
    s3_url TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/najam009/Dev-QA.git
cd Dev-QA
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:

```env
# AWS Configuration
BUCKET_NAME=your-s3-bucket-name
AWS_REGION=ap-south-1

# PostgreSQL Configuration
HOST=your-database-host
DBNAME=your-database-name
USERR=your-database-user
PASSWORD=your-database-password
PORT=5432
```

### 4. Configure AWS Credentials
Ensure AWS credentials are configured:
```bash
aws configure
```

Or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
```

## ⚙️ Configuration

### Modify Watch Folder Path
Edit the `FOLDER_TO_WATCH` variable in your chosen script:

```python
FOLDER_TO_WATCH = "/home/najam/S3bucket/"  # Change to your path
```

### S3 Bucket Configuration
Update the bucket name in your `.env` file or directly in the script:

```python
BUCKET_NAME = "your-bucket-name"
AWS_REGION = "your-region"  # e.g., us-east-1, ap-south-1
```

### Database Configuration
Update database credentials in `.env` file (recommended) or `DB_CONFIG` dictionary:

```python
DB_CONFIG = {
    "host": "localhost",
    "dbname": "mydb",
    "user": "myuser",
    "password": "mypassword",
    "port": 5432
}
```

## 💻 Usage

### Option 1: Local Folder Monitoring Only
```bash
python local_watcher.py
```
- Monitors local folder
- Prints file events to console
- No S3 or database integration

### Option 2: S3 Synchronization Only
```bash
python s3_watcher.py
```
- Monitors local folder
- Syncs with S3 bucket
- No database logging

### Option 3: Full Stack (Recommended)
```bash
python s3_database.py
```
- Monitors local folder
- Syncs with S3 bucket
- Logs all operations to PostgreSQL

### Running in Background
```bash
# Linux/Mac
nohup python s3_database.py > app.log 2>&1 &

# Windows (PowerShell)
Start-Process python -ArgumentList "s3_database.py" -WindowStyle Hidden
```

## 📁 Project Structure

```
Dev-QA/
├── .git/                    # Git repository
├── .gitignore              # Git ignore patterns
├── Dockerfile              # Docker container definition
├── requirements.txt        # Python dependencies
├── trigger.txt            # Trigger file for testing
├── local_watcher.py       # Basic file monitoring
├── s3_watcher.py          # S3 sync without database
├── s3_database.py         # Full S3 + database sync
└── README.md              # This file
```

## 🔐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BUCKET_NAME` | S3 bucket name | `my-files-bucket` |
| `AWS_REGION` | AWS region | `ap-south-1` |
| `HOST` | PostgreSQL host | `localhost` or `your-rds-endpoint.amazonaws.com` |
| `DBNAME` | Database name | `file_tracker` |
| `USERR` | Database user | `postgres` |
| `PASSWORD` | Database password | `secretpassword` |
| `PORT` | Database port | `5432` |

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t dev-qa-app .
```

### Run Container
```bash
docker run -d \
  --name dev-qa \
  -v /local/path/to/watch:/home/najam/S3bucket \
  --env-file .env \
  dev-qa-app
```

### Docker Compose (Optional)
Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  dev-qa:
    build: .
    container_name: dev-qa-sync
    volumes:
      - /local/path:/home/najam/S3bucket
    env_file:
      - .env
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. **Access Denied (S3)**
```
Error: An error occurred (AccessDenied) when calling PutObject
```
**Solution**: Check IAM permissions and AWS credentials

#### 2. **Database Connection Failed**
```
Error: could not connect to server
```
**Solution**: Verify PostgreSQL is running and credentials are correct

#### 3. **Folder Not Being Watched**
```
No output when files change
```
**Solution**: Ensure `FOLDER_TO_WATCH` path exists and is correct

#### 4. **Module Not Found**
```
ModuleNotFoundError: No module named 'boto3'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Debug Mode
Add verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Branch Strategy
- `main` - Production-ready code
- `dev` - Development branch with CI/CD
- `qa` - QA testing branch with CI/CD

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [@najam009](https://github.com/najam009)

## 🔄 Branches Overview

This repository uses a branch-based workflow:
- **main**: Stable release branch (you are here)
- **dev**: Active development with automated CI/CD to dev environment
- **qa**: Quality assurance testing with automated CI/CD to QA environment

---

**Made with ❤️ by najam009**
