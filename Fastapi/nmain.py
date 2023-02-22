from fastapi import FastAPI,HTTPException,status,Path
from pydantic import BaseModel
# from backend.utils import hashing, JWT_token
# from backend.awscloud.s3 import main as aws
# from data import user
# from schemas import User, GOES
# from oauth2 import get_current_user

from datetime import date


app = FastAPI()

class UserInput(BaseModel):
    year : int
    month :int
    station :str
    filename:str
    #date: date

#apirouter for nexrad

# router = APIRouter(
#     prefix='/goes',
#     tags=['NEXRAD 18']
# )


#sample
@app.get("/say hello")
def say_hello():
    return {"message":"Hello World"}

#for inputing the date directly(GETTING THE DATE INPUT FROM STREAMLIT)
@app.get("/get-date/{year}/{month}/{day}")
@app.get("/getting the date values")
def get_date(year: int, month: int, day: int):
    try:
        date_obj = date(year, month, day)
        return {"date": str(date_obj)}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please enter the right value'.")

@app.get("/getting the date values")
def get_date(year: int, month: int, day: int):
    try:
        date_obj = date(year, month, day)
        return {"date": str(date_obj)}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use the format 'YYYY-MM-DD'.")

# @router.get('/files/')
# def get_all_nexrad_file(station: str, year: str, day: str, response: Response, get_current_user:User = Depends(get_current_user)):
#     # Code to retrieve from filename form SQL Lite DB.

#     return "done"


#checking if the station is existing in the db

station = ["KABR"]#station data from DB

@app.get("/checking if the station exists in the db/{station}")
async def validate_string(station: str = Path(..., description="Validating stations", regex="|".join(station))):
    if validate_string not in station:
        raise HTTPException(status_code=404, detail="Station not found")
    return {"station": station}

#for getting the url with the date,time and station from the user
@app.post("/fetch_url")
def fetch_url(userinput: UserInput):
    if userinput.station == int:
        raise HTTPException(status_code =404, detail="Item Not found, Enter a valid station name")

    elif (userinput.date == 2024):
        raise HTTPException(status_code =402, detail="Bad Request, Enter a valid date")

    elif (userinput.date == 32):
        raise HTTPException(status_code = 402, detail ="Bad Request,Enter a valid date")

    aws_nexrad_url = f'https://noa-nexrad-level2.s3.amazonaws.com/index.html#{userinput.year:04}/{userinput.month:02}/{userinput.date:02}/{userinput.station:04}'
    return {'url': aws_nexrad_url}



# @router.post('/generate/aws-link', status_code=status.HTTP_201_CREATED)
# def generate_aws_link(request: NEXRAD, get_current_user:User = Depends(get_current_user)):
    
#     team_link, goes_link = aws.get_geos_aws_link(app.station, app.year, app.day, app.file_name)
    
#     return {
#         'success':True,
#         'message':'link generated',
#         'team_link':team_link,
#         'goes_link':nexrad_link
#     }
