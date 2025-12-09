from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    MONGODB_URI: str
    DATABASE_NAME: str = "progress_hub"
    CLERK_SECRET_KEY: str = ""
    CLERK_ISSUER: str = "" # URL of the Clerk instance (e.g., https://clerk.your-domain.com or https://api.clerk.com/v1/...)
    CLERK_PEM_PUBLIC_KEY: str = "" # Optional if using PEM directly
    SUPER_ADMIN_EMAIL: str = ""

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
