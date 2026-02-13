"""Application Configuration"""

from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application Settings"""
    
    # Application
    APP_NAME: str = "AI Enterprise Operating System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Database - SQLAlchemy/SQLite (Streamlit Cloud compatible)
    DATABASE_URL: str = "sqlite:///./data/ai_enterprise.db"
    
    # Database - MongoDB
    MONGODB_HOST: str = "localhost"
    MONGODB_PORT: int = 27017
    MONGODB_DB: str = "ai_enterprise_mongo"
    MONGODB_USER: str = "mongo"
    MONGODB_PASSWORD: str = "mongo_password"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # JWT Authentication
    JWT_SECRET_KEY: str = "your-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ML Models
    MODEL_STORAGE_PATH: str = "./models"
    MODEL_VERSION: str = "1.0.0"
    
    # Cloud Provider
    CLOUD_PROVIDER: str = "aws"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    
    @property
    def sqlalchemy_database_url(self) -> str:
        """Get SQLAlchemy database URL and ensure local SQLite path exists."""
        if self.DATABASE_URL.startswith("sqlite:///"):
            raw_path = self.DATABASE_URL.replace("sqlite:///", "", 1)
            db_path = Path(raw_path)
            if not db_path.is_absolute():
                db_path = Path.cwd() / db_path
            db_path.parent.mkdir(parents=True, exist_ok=True)
        return self.DATABASE_URL
    
    @property
    def mongodb_url(self) -> str:
        """Get MongoDB connection URL"""
        return f"mongodb://{self.MONGODB_USER}:{self.MONGODB_PASSWORD}@{self.MONGODB_HOST}:{self.MONGODB_PORT}/{self.MONGODB_DB}"
    
    @property
    def redis_url(self) -> str:
        """Get Redis connection URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
