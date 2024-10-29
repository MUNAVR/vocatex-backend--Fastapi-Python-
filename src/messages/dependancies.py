from fastapi import Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException


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
    
async def get_user_id_from_token(token: str):
    token_data = decode_token(token)
    user_id = token_data.get("user_id")
    print("getuserfunction",user_id)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User ID not found in token")
    return user_id