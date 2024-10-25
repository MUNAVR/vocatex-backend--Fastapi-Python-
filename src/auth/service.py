from .models import User,ProviderUser
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import *

class UserService:
    async def get_user_by_email(self,email:str ,session:AsyncSession):

        statement=select(User).where(User.email==email)
        result=await session.exec(statement)

        user=result.first()

        return user
    
    async def exist_user(self,email:str,session:AsyncSession):
        user= await self.get_user_by_email(email,session)

        return True if user is not None else False
    
    async def create_user(self,user_details:UserCreateModel,session:AsyncSession):
        user_data_dict=user_details.model_dump()

        otp = generate_otp() 
        otp_created_at = datetime.utcnow() 

        new_user=User(
            **user_data_dict,
            otp=otp,
            otp_created_at=otp_created_at

        )

        new_user.password_hash= generate_passwd_hash(user_data_dict['password'])

        session.add(new_user)
        await session.commit()
        await send_otp_email(new_user.email, otp)

        return new_user
    

    async def verify_otp(self, email: str, otp: str, session: AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.first()

        if not user:
            return None  

        # Verify the OTP and expiration time (10-minute expiration)
        if user.otp == otp and datetime.utcnow() - user.otp_created_at < timedelta(minutes=10):
            user.is_verified = True
            user.otp = " "  # Clear OTP after verification
            session.add(user)
            await session.commit()
            return user
        else:
            return None

    async def send_reset_password_otp(self, email: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        if not user:
            return None  # User not found

        otp = generate_otp()
        otp_created_at = datetime.utcnow()

        user.otp = otp
        user.otp_created_at = otp_created_at

        session.add(user)
        await session.commit()

        await send_reset_password_otp_email(user.email, otp)
        return user
    

    async def verify_reset_password_otp(self, email: str, otp: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        if not user:
            return None  # User not found

        # Check if OTP is correct and within expiration time (10 minutes)
        if user.otp == otp and datetime.utcnow() - user.otp_created_at < timedelta(minutes=10):
            return user  # OTP is valid
        return None  # OTP invalid or expired
    
    

    async def reset_password(self, email: str, new_password: str, session: AsyncSession):
        user = await self.get_user_by_email(email, session)
        if not user:
            return None  # User not found

        user.password_hash = generate_passwd_hash(new_password)
        user.otp = " "  # Clear OTP after reset
        session.add(user)
        await session.commit()
        return user




class ProviderUserService:
    async def get_user_by_email(self,email:str ,session:AsyncSession):

        statement=select(ProviderUser).where(ProviderUser.email==email)
        result=await session.exec(statement)

        user=result.first()

        return user
    
    async def exist_user(self,email:str,session:AsyncSession):
        user= await self.get_user_by_email(email,session)

        return True if user is not None else False
    
    async def create_user(self,user_details:UserCreateModel,session:AsyncSession):
        user_data_dict=user_details.model_dump()

        otp = generate_otp() 
        otp_created_at = datetime.utcnow() 

        new_user=ProviderUser(
            **user_data_dict,
            otp=otp,
            otp_created_at=otp_created_at
        )

        new_user.password_hash= generate_passwd_hash(user_data_dict['password'])

        session.add(new_user)
        await session.commit()
        await send_otp_email(new_user.email, otp)

        return new_user
    
    async def verify_otp(self, email: str, otp: str, session: AsyncSession):
        print("1")
        statement = select(ProviderUser).where(ProviderUser.email == email)
        result = await session.exec(statement)
        user = result.first()

        if not user:
            return None  

        # Verify the OTP and expiration time (10-minute expiration)
        if user.otp == otp and datetime.utcnow() - user.otp_created_at < timedelta(minutes=10):
            user.is_verified = True
            user.otp = " "  # Clear OTP after verification
            session.add(user)
            await session.commit()
            return user
        else:
            return None