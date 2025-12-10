from beanie import Document
from pydantic import EmailStr
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    MANAGER = "manager"
    DEVELOPER = "developer"
    LEADERSHIP = "leadership"

class User(Document):
    email: EmailStr
    name: str
    password_hash: str
    role: UserRole = UserRole.DEVELOPER
    
    class Settings:
        name = "users"
