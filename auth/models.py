from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    content: str = Field(default=None)


class UserSchema(BaseModel):
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)


class UserLoginSchema(BaseModel):
    username: str = Field(default=None)
    password: str = Field(default=None)


class TokenData(BaseModel):
    username: str = Field(default=None)
    email: EmailStr = Field(default=None)
