"""
Application configuration settings
"""
import os
from typing import Optional


class Settings:
    """Application settings configuration"""
    
    # API Configuration
    API_TITLE: str = "Mule Cracks"
    API_DESCRIPTION: str = "API to scan MuleSoft projects and show dependency versions from pom.xml files"
    API_VERSION: str = "1.0.0"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # MuleSoft Projects Configuration
    MULE_DIRECTORY: str = "/Users/gelvy-mondestin.myssie-bingha/Documents/mule"
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    
    @classmethod
    def get_mule_directory(cls) -> str:
        """Get MuleSoft projects directory path"""
        return os.getenv("MULE_DIRECTORY", cls.MULE_DIRECTORY)
    
    @classmethod
    def get_host(cls) -> str:
        """Get server host"""
        return os.getenv("HOST", cls.HOST)
    
    @classmethod
    def get_port(cls) -> int:
        """Get server port"""
        return int(os.getenv("PORT", cls.PORT))
    
    @classmethod
    def get_reload(cls) -> bool:
        """Get reload setting"""
        return os.getenv("RELOAD", "true").lower() == "true"


# Global settings instance
settings = Settings() 