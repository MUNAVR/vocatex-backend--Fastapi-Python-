from fastapi import Request, status,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.service import UserService


userService=UserService()

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
       
        cred = await super().__call__(request)
        token = cred.credentials

        
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        
        token_data = decode_token(token)

       
        if 'refresh' in token_data and token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token, not a refresh token"
            )

        
        return token_data

    def token_valid(self, token: str) -> bool:
        
        token_data = decode_token(token)
        return token_data is not None


    
async def get_currnt_user(token_details:dict = Depends(AccessTokenBearer()),
                    session:AsyncSession = Depends(get_session),
                    ):
    user_email=token_details['user']['email']

    user = await userService.get_user_by_email(user_email,session)

    return user