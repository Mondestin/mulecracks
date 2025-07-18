"""
Entry point for the MuleSoft Connector Scanner API
"""
from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.config.settings import settings
    
    uvicorn.run(
        "app.main:app",
        host=settings.get_host(),
        port=settings.get_port(),
        reload=settings.get_reload()
    ) 