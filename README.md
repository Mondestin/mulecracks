# Mule Cracks

A FastAPI application that scans MuleSoft projects and analyzes flows, endpoints, and processors.

## Overview

This API scans MuleSoft projects and extracts:
- **Flows**: Flow names, HTTP methods, and paths
- **Endpoints**: HTTP endpoints with methods and paths
- **Processors**: Count and names of all processors in each flow
- **Dependencies**: Version information from pom.xml files

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

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /mule/dependencies` - Scan dependencies from pom.xml files
- `GET /mule/flows` - Scan flows and extract endpoints/processors

## Configuration

Set the MuleSoft projects directory path:
```bash
export MULE_DIRECTORY="/path/to/your/mule/projects"
```

## Features

- **Flow Detection**: Extracts flow names and HTTP endpoints
- **Processor Analysis**: Counts and identifies all processors in flows
- **Dependency Scanning**: Analyzes pom.xml files for version information
- **Error Handling**: Properly handles MuleSoft error structures 