from typing import Union
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


## Declaring input user names & password:
name = ['person 1', 'person 2']
u_name = ['pp','cc']
password = ['123','321']

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None

class User(BaseModel):
    name : str
    email : str
    password : str

class Login(BaseModel):
    uname : str 
    password : str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login(request: Login):
    if Login.uname not in u_name:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f"Invalid Credentials")
        
    return Login.uname