from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class Register(BaseModel):
    username: str = Field(min_length=3, max_length=40, pattern=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=128)

class Login(BaseModel):
    email: EmailStr
    password: str

class ProfileUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=100)
    bio: str | None = Field(default=None, max_length=1000)

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: EmailStr
    full_name: str
    bio: str | None
    avatar_url: str | None
    created_at: datetime

class PublicUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    full_name: str
    bio: str | None
    avatar_url: str | None

class PostCreate(BaseModel):
    content: str = Field(min_length=1, max_length=5000)

class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    content: str
    image_url: str | None
    created_at: datetime

class CommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)

class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime
