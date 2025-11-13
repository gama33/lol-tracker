import os
from typing import List

class Settings:
    APP_NAME: str = "LOL Tracker API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./lol_tracker.db")
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW: int = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_RECYCLE: int = int(os.getenv("DB_POOL_RECYCLE", "3600"))
    SQL_ECHO: bool = os.getenv("SQL_ECHO", "false").lower() == "true"

    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000"
    ]

    RIOT_API_KEY: str = os.getenv("RIOT_API_KEY", "")
    RIOT_REGION: str = os.getenv("RIOT_REGION", "americas")
    RIOT_PLATFORM: str = os.getenv("RIOT_PLATFORM", "br1")

settings = Settings()