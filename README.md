# Mule Cracks

A FastAPI application that scans MuleSoft projects and extracts dependency versions from pom.xml files.

## Overview

This API scans all MuleSoft projects in a specified directory and returns dependency information including versions, group IDs, artifact IDs, and other metadata from their pom.xml files.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health
   - Dependencies: http://localhost:8000/mule/dependencies

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /mule/dependencies` - Scan MuleSoft projects and return dependency data

## Configuration

Set the MuleSoft projects directory path:
```bash
export MULE_DIRECTORY="/path/to/your/mule/projects"
``` 