from fastapi import APIRouter, status, HTTPException, Response, Depends
from pydantic import BaseModel

from .. import hashing
from .. import JWT_token
from .. data import user
from .. schemas import User
from fastapi.security import OAuth2PasswordRequestForm
import os

router = APIRouter(
    prefix='/user',
    tags=['User']
)
userDB = user.User()



@router.post('/sign-up', status_code=status.HTTP_201_CREATED)
def sign_up_user(request: User, response: Response):
    
    is_user_created = userDB.insert_new_user(request.username, hashing.Hash().get_hashed_password(request.password))

    if(is_user_created == False):
       raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")
    

    return {
        'success': True,
        'message': 'user created successfully'
    }


@router.post('/login', status_code=status.HTTP_200_OK)
def sign_in_user(request: OAuth2PasswordRequestForm = Depends()):
    user = userDB.find_username(request.username)

    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="username not found")
    
    # hashed_pass = hashing.Hash().get_hashed_password(request.password)

    if not hashing.Hash().verify_password(user['password'], request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentioals")
    
    access_token = JWT_token.create_access_token(data={"id": user['id'], "username": user['username']})
    
    return {"username": user['username'], "access_token": access_token, "token_type": "bearer"}
    

