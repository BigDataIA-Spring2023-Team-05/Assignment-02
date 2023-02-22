from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    password: str



class GOES(BaseModel):
    station: str
    year: str
    day: str
    hour: str
    file_name:str