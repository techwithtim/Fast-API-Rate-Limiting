from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.models import Token, User, UserResponse
from app.auth import authenticate_user, create_access_token, get_current_user
from app.config import settings, limiter
from app.database import get_user, add_user
from app.auth import pwd_context
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

router = APIRouter()

def rate_limit_key_func(request: Request):
    user = request.state.user if hasattr(request.state, 'user') else None
    return f"{request.client.host}:{user.username if user else 'anonymous'}"

@router.post("/token", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponse)
@limiter.limit("3/hour")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if get_user(username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    hashed_password = pwd_context.hash(password)
    logger.debug(f"Adding user: {username}")
    new_user = add_user(username, hashed_password)
    logger.debug(f"New user: {new_user}")
    
    if new_user is None:
        logger.error("Failed to add user")
        raise HTTPException(
            status_code=500,
            detail="Failed to create user"
        )
    
    return UserResponse(username=new_user.username)

@router.get("/users/me")
@limiter.limit("10/minute", key_func=rate_limit_key_func)
async def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    request.state.user = current_user
    return current_user

@router.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "Hello World"}
