from pydantic import BaseModel, EmailStr
from datetime import datetime

# Post Pydantic schemas
class PostCreate(BaseModel):
    post_id: int
    post_data: str
    user_id: str

class PostResponse(BaseModel):
    post_id: int
    post_data: str
    user_id: str
    class Config:
        from_attributes = True

# User Pydantic schemas
class UserCreate(BaseModel):
    user_id: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    password: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None
    
class UserLogin(BaseModel):
    user_id: str
    password: str

class Vote(BaseModel):
    post_id: int
    dir: int  # 1 for upvote, 0 for remove vote