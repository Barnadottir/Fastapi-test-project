# history | grep fastapi
# fastapi dev api.py

from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from pydantic import BaseModel
import jwt
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with your frontend's URL in production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all headers, including custom ones like `token`
)

# Secret key for encoding/decoding JWT tokens
SECRET_KEY = "your_secret_key"  # Replace with a secure key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Sample user data (replace with actual user management in production)
fake_users_db = {
    "user": {"password": "password"}
}

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str

class UserInDB(User):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    testparamter: str | None = None

class AuthHeader(BaseModel):
    token: str

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verify JWT token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return TokenData(username=username)
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Login endpoint to generate token
@app.post("/token", response_model=Token)
def login(login_data: UserLogin):
    print(f'userdata {login_data}')
    user = fake_users_db.get(login_data.username)
    if user is None or user["password"] != login_data.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": login_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get the current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    return token_data

# Protected route
@app.get("/protected")
def protected_route(
    headers: Annotated[AuthHeader, Header()],
):
    print(f'headers -> {headers}')
    return {'message': 'successfully entered route'}


@app.post('/change_username')
def change_username(
    headers: Annotated[AuthHeader, Header()],
)
