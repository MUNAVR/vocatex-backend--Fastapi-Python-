from passlib.context import CryptContext
from datetime import datetime,timedelta
import jwt
from src.config import Config
import uuid
import logging
import utils
import random
import string
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

conf = ConnectionConfig(
    MAIL_USERNAME="munavarmjp@gmail.com",  
    MAIL_PASSWORD="bcnz owta nucw wwqw",  
    MAIL_SERVER="smtp.gmail.com", 
    MAIL_PORT=587, 
    MAIL_FROM="munavarmjp@gmail.com", 
    MAIL_FROM_NAME="Vocotex", 
    MAIL_STARTTLS=True, 
    MAIL_SSL_TLS=False 
)

async def send_otp_email(email: str, otp: str):
    template = Template("""
    <h3>Welcome to Vocatex</h3>
    <p>Your One-Time Password (OTP) for email verification is: <strong>{{ otp }}</strong></p>
    <p>It will expire in 10 minutes.</p>
    """)
    html = template.render(otp=otp)

    message = MessageSchema(
        subject="Email Verification OTP",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    

async def send_reset_password_otp_email(email: str, otp: str):
    template = Template("""
    <h3>Password Reset Request</h3>
    <p>Your OTP for resetting the password is: <strong>{{ otp }}</strong></p>
    <p>It will expire in 10 minutes.</p>
    """)
    html = template.render(otp=otp)

    message = MessageSchema(
        subject="Password Reset OTP",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)



password_context= CryptContext(
    schemes=['bcrypt']
)



def generate_passwd_hash(password:str):
    hash=password_context.hash(password)

    return hash


def verify_password(password:str,hash:str):
    return  password_context.verify(password,hash)


ACCESS_TOKEN_EXPIRY = 3600

def create_access_token(user_data : dict, expiry : timedelta=None, refresh :bool= False):

    payload={}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload = payload,
        key = Config.JWT_SECRET,
        algorithm = Config.JWT_ALOGRITHM
    )

    return token

def decode_token(token:str):
    try:
        token_data = jwt.decode(
            jwt = token,
            key = Config.JWT_SECRET,
            algorithms = Config.JWT_ALOGRITHM
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

