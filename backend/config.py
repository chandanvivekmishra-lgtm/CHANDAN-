"""Configuration management for the NIDS backend."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # Database
    database_url: str = "postgresql://nids_user:nids_pass@localhost:5432/nids_db"
    database_echo: bool = False
    
    # API
    api_title: str = "NIDS API"
    api_version: str = "1.0.0"
    debug: bool = True
    secret_key: str = "supersecret"
    
    # ML Model Configuration
    model_path: str = "./models/detection_model.pkl"
    scaler_path: str = "./models/scaler.pkl"
    anomaly_threshold: float = 0.8
    
    class Config:
        env_file = "../config/.env"
        case_sensitive = False


settings = Settings()
