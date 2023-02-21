from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import List, Union
import os
from dotenv import load_dotenv

load_dotenv()

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm = os.environ.get('ALGORITHM'))
    return encoded_jwt