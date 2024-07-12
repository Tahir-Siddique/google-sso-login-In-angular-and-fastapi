import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi_sso.sso.google import GoogleSSO
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
REDIRECT_URL = os.getenv("REDIRECT_URL")
LOCALHOST_URL = os.getenv("LOCALHOST_URL")

google_sso = GoogleSSO(
    os.getenv("GOOGLE_CLIENT_ID"), 
    os.getenv("GOOGLE_CLIENT_SECRET"), 
    LOCALHOST_URL+"/auth/callback"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    roles: List[str]

@app.get("/login/google")
async def google_login():
    return await google_sso.get_login_redirect()

@app.get("/auth/callback")
async def google_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Code not found")
    try:
        user = await google_sso.verify_and_process(request)
    except Exception as e:
        logging.error(f"Error processing login: {e}")
        raise HTTPException(status_code=400, detail="Error processing login")

    token = jwt.encode({"sub": user.id, "roles": ["viewer"]}, SECRET_KEY, algorithm=ALGORITHM)
    response = RedirectResponse(url=f"{REDIRECT_URL}/home?token={token}")
    response.set_cookie("access_token", token)
    return response

@app.get("/user/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        return {"username": username, "roles": roles}
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
