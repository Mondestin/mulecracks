# MuleSoft Dependency Scanner API

A production-ready FastAPI application that scans MuleSoft projects and extracts dependency versions from pom.xml files.

## 🏗️ Architecture

This project follows Object-Oriented Programming principles with a clean, modular architecture:

```
mulegrade/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── api/                      # API layer
│   │   ├── __init__.py
│   │   └── routes.py             # API routes and endpoints
│   ├── config/                   # Configuration layer
│   │   ├── __init__.py
│   │   └── settings.py           # Application settings
│   ├── models/                   # Data models layer
│   │   ├── __init__.py
│   │   └── connector.py          # Pydantic models
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   └── mule_scanner.py       # MuleSoft project scanning service
│   └── utils/                    # Utilities layer
│       ├── __init__.py
│       └── xml_parser.py         # XML parsing utilities
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore file
└── README.md                     # This file
```

## 🚀 Features

- ✅ **Production-ready architecture** with proper separation of concerns
- ✅ **Object-Oriented Design** with clean, maintainable code
- ✅ **Configuration management** with environment variable support
- ✅ **Comprehensive logging** for debugging and monitoring
- ✅ **Error handling** with proper HTTP status codes
- ✅ **CORS middleware** for cross-origin requests
- ✅ **Automatic API documentation** (Swagger UI & ReDoc)
- ✅ **Type hints** throughout the codebase
- ✅ **Modular design** for easy testing and maintenance

## 📋 API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /mule/dependencies` - Scan MuleSoft projects and return dependency data

## 🛠️ Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd mulegrade
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application

### Development Mode
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Using the entry point
```bash
python main.py
```

## 🔧 Configuration

The application uses a centralized configuration system in `app/config/settings.py`. You can override settings using environment variables:

```bash
export MULE_DIRECTORY="/path/to/your/mule/projects"
export HOST="0.0.0.0"
export PORT="8000"
export RELOAD="false"
```

## 📊 API Documentation

Once the server is running, access:

- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc

## 🧪 Example Usage

### Get MuleSoft Dependency Information
```bash
curl -X GET "http://localhost:8000/mule/dependencies"
```

### Response Structure
```json
{
  "total_projects": 6,
  "projects": [
    {
      "project_name": "customers-sapi-app-1.0.0-mule-application",
      "project_path": "/Users/gelvy-mondestin.myssie-bingha/Documents/mule/customers-sapi-app-1.0.0-mule-application",
      "group_id": "968a3b4a-2d36-49fd-af6b-de8e444c6a5b",
      "artifact_id": "customers-sapi-app",
      "version": "1.0.0",
      "packaging": "mule-application",
      "app_runtime": "4.8.0",
      "mule_maven_plugin_version": "4.3.0",
      "dependencies": [
        {
          "group_id": "org.mule.connectors",
          "artifact_id": "mule-http-connector",
          "version": "1.10.0",
          "classifier": "mule-plugin",
          "scope": null
        }
      ]
    }
  ]
}
```

## 🏗️ Architecture Details

### Layers

1. **API Layer** (`app/api/`): Handles HTTP requests and responses
2. **Service Layer** (`app/services/`): Contains business logic
3. **Model Layer** (`app/models/`): Data models and validation
4. **Config Layer** (`app/config/`): Application configuration
5. **Utils Layer** (`app/utils/`): Reusable utilities

### Key Classes

- **`MuleProjectScanner`**: Main service class for scanning MuleSoft projects
- **`XMLParser`**: Utility class for parsing pom.xml files
- **`Settings`**: Configuration management class
- **`DependencyInfo`**, **`ProjectInfo`**: Data models for API responses

## 🔍 Logging

The application includes comprehensive logging configured in `app/main.py`. Logs include:
- Application startup/shutdown events
- Error handling and debugging information
- API request processing

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment Variables**: Configure all settings via environment variables
2. **Logging**: Configure proper log levels and output destinations
3. **CORS**: Restrict CORS origins to your frontend domains
4. **Security**: Add authentication and authorization if needed
5. **Monitoring**: Add health checks and monitoring endpoints
6. **Containerization**: Use Docker for consistent deployment

## 📝 Development

### Adding New Features

1. **Models**: Add new Pydantic models in `app/models/`
2. **Services**: Add business logic in `app/services/`
3. **Routes**: Add new endpoints in `app/api/routes.py`
4. **Utils**: Add reusable utilities in `app/utils/`

### Testing

The modular architecture makes it easy to add unit tests for each layer.

## 📄 License

This is a production-ready MuleSoft dependency scanner API. 