from fastapi import APIRouter, status, HTTPException, Response, Depends
from pydantic import BaseModel
from backend.utils import hashing, JWT_token
from data import user
import os
from schemas import User, GOES
from oauth2 import get_current_user
from backend.awscloud.s3 import main as aws

router = APIRouter(
    prefix='/goes',
    tags=['GOES 18']
)



@router.get('/files/')
def get_all_goes_file(station: str, year: str, day: str, hour: str, response: Response, get_current_user:User = Depends(get_current_user)):
    # Code to retrieve from filename form SQL Lite DB.

    return "done"

@router.post('/generate/aws-link', status_code=status.HTTP_201_CREATED)
def generate_aws_link(request: GOES, get_current_user:User = Depends(get_current_user)):
    
    team_link, goes_link = aws.get_geos_aws_link(request.station, request.year, request.day, request.hour, request.file_name)
    
    return {
        'success':True,
        'message':'link generated',
        'team_link':team_link,
        'goes_link':goes_link
    }