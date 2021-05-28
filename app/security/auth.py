from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(
	prefix="/auth"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/hello")
async def hello(token: str =  Depends(oauth2_scheme)):
	return {"token": token}
