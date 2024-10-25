from fastapi import APIRouter,Depends,status
from .schemas import *
from .service import UserService,ProviderUserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import *
from datetime import datetime,timedelta
from fastapi.responses import  JSONResponse
from src.auth.dependencies import AccessTokenBearer
from jose import jwt
import requests


auth_router = APIRouter()
user_service = UserService()
provider_service=ProviderUserService()
access_token_bearar = AccessTokenBearer()
REFRESH_TOKEN_EXPIRY = 2
GOOGLE_CLIENT_ID = "897102232394-gdqdtqogo6nbno5194t9g7svvd885ojo.apps.googleusercontent.com"

@auth_router.post('/signup',response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession = Depends(get_session)):

    email=user_data.email

    user_exists = await user_service.exist_user(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User with email already exisits")
    
    new_user = await user_service.create_user(user_data,session)
    return new_user



@auth_router.post("/verify-otp")
async def verify_otp(otp_data: OTPVerifyModel, session: AsyncSession = Depends(get_session)):
    user_service = UserService()
    user = await user_service.verify_otp(otp_data.email, otp_data.otp, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP or OTP expired")

    return {"message": "Email successfully verified."}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@auth_router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, session: AsyncSession = Depends(get_session)):
    email = request.email
    print(email)
    user = await user_service.send_reset_password_otp(email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "OTP sent to your email for password reset"}


@auth_router.post("/verify-reset-password-otp")
async def verify_reset_password_otp(otp_data: OTPVerifyModel, session: AsyncSession = Depends(get_session)):
    print(otp_data)
    user = await user_service.verify_reset_password_otp(otp_data.email, otp_data.otp, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP or OTP expired")

    return {"message": "OTP verified, you can now reset your password."}



@auth_router.post("/reset-password")
async def reset_password(data: ResetPasswordModel,session: AsyncSession = Depends(get_session)):
    email = data.email
    new_password = data.new_password
    print(email)
    user = await user_service.reset_password(email, new_password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {"message": "Password successfully reset."}



@auth_router.post('/login')
async def login_user(login_data:UserLoginModel,session:AsyncSession = Depends(get_session)):
    email=login_data.email
    password=login_data.password

    user = await user_service.get_user_by_email(email,session)

    if user is not None:
        password_valid=verify_password(password,user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message":"Login succesfull",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)

                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email  or Password"
    )




class GoogleLoginPayload(BaseModel):
    token: str

def verify_google_token(token: str):
    # Send request to Google to verify the token
    response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
    if response.status_code != 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    
    token_info = response.json()

    if token_info['aud'] != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token's audience doesn't match")
    
    return token_info


@auth_router.post('/google-login')
async def google_login(google_payload: GoogleLoginPayload, session: AsyncSession = Depends(get_session)):
    token_info = verify_google_token(google_payload.token)

    email = token_info.get('email')
    name = token_info.get('name')
    picture = token_info.get('picture')

    # Check if user exists in the database
    user = await user_service.get_user_by_email(email, session)

    if user is None:
        # If user does not exist, create a new user
        user_data = UserCreateModel(
            username=name,
            email=email,
            password="123123"  # No password since it's a Google account
        )
        user = await user_service.create_user(user_data, session)

    # Generate tokens (same as regular login)
    access_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid)
        }
    )

    refresh_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid)
        },
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid),
                
            }
        }
    )




# provider--------------------------------------------------------------------

@auth_router.post('/provider/signup',response_model=UserModel,status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data:UserCreateModel,session:AsyncSession = Depends(get_session)):

    email=user_data.email

    user_exists = await provider_service.exist_user(email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="User with email already exisits")
    
    new_user = await provider_service.create_user(user_data,session)
    return new_user

@auth_router.post("/provider/verify-otp")
async def verify_otp(otp_data: OTPVerifyModel, session: AsyncSession = Depends(get_session)):
    print("here")

    user = await provider_service.verify_otp(otp_data.email, otp_data.otp, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP or OTP expired")

    return {"message": "Email successfully verified."}

@auth_router.post('/provider/login')
async def login_user(login_data:UserLoginModel,session:AsyncSession = Depends(get_session)):
    email=login_data.email
    password=login_data.password

    user = await provider_service.get_user_by_email(email,session)

    if user is not None:
        password_valid=verify_password(password,user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                }
            )

            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_uid':str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message":"Login succesfull",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user":{
                        "email":user.email,
                        "uid":str(user.uid)

                    }
                }
            )
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email  or Password"
    )



@auth_router.post('/provider/google-login')
async def google_login(google_payload: GoogleLoginPayload, session: AsyncSession = Depends(get_session)):
    token_info = verify_google_token(google_payload.token)

    email = token_info.get('email')
    name = token_info.get('name')
    picture = token_info.get('picture')

    # Check if user exists in the database
    user = await provider_service.get_user_by_email(email, session)

    if user is None:
        # If user does not exist, create a new user
        user_data = UserCreateModel(
            username=name,
            email=email,
            password="123123"  # No password since it's a Google account
        )
        user = await provider_service.create_user(user_data, session)

    # Generate tokens (same as regular login)
    access_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid)
        }
    )

    refresh_token = create_access_token(
        user_data={
            'email': user.email,
            'user_uid': str(user.uid)
        },
        refresh=True,
        expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
    )

    return JSONResponse(
        content={
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "email": user.email,
                "uid": str(user.uid),
                
            }
        }
    )