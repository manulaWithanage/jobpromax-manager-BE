from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union

class Settings(BaseSettings):
    MONGODB_URI: str
    DATABASE_NAME: str = "progress_hub"
    
    # JWT Settings
    JWT_SECRET: str = "change-this-secret-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days (10080 minutes)
    
    ALLOWED_ORIGINS: Union[List[str], str] = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    def parse_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
