from pydantic import BaseModel,Field,EmailStr
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    username:str 
    email:EmailStr 
    password:str


class OTPVerifyModel(BaseModel):
    email: EmailStr
    otp: str


class UserModel(BaseModel):
    uid: uuid.UUID 
    username:str
    email:str
    is_verified:bool 
    password_hash:str = Field(exclude=True)
    created_at:datetime
    updated_at:datetime

class UserLoginModel(BaseModel):
    email:str
    password:str

class ResetPasswordModel(BaseModel):
    email: EmailStr
    new_password: str

