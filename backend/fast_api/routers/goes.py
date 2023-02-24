from fastapi import APIRouter, status, HTTPException, Response, Depends
from pydantic import BaseModel
from .. data import user
import os
from .. schemas import User, GOES
from .. oauth2 import get_current_user
from awscloud.s3 import main as aws
import re

router = APIRouter(
    prefix='/goes',
    tags=['GOES 18']
)



@router.get('/files')
def get_all_goes_file(station: str, year: str, day: str, hour: str, response: Response, get_current_user:User = Depends(get_current_user)):
    # Code to retrieve from filename form SQL Lite DB.
    result = aws.get_all_geos_file_name_by_filter(station=station, year=year, day=day, hour=hour)

    return {
        'success':True,
        'all_files': result
    }

@router.post('/generate/aws-link', status_code=status.HTTP_201_CREATED)
def generate_aws_link(request: GOES, get_current_user:User = Depends(get_current_user)):
    
    result = aws.get_geos_aws_link(request.station, request.year, request.day, request.hour, request.file_name)
    
    if(result == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested file does not exists!")

    team_link, goes_link = result

    return {
        'success':True,
        'message':'link generated',
        'team_link':team_link,
        'goes_link':goes_link
    }


@router.post('/generate/aws-link-by-filename/{filename}', status_code=status.HTTP_201_CREATED)
def generate_aws_link_by_filename(filename, get_current_user:User = Depends(get_current_user)):
    
    regex = re.compile(r'(OR)_(ABI)-(L\d+b)-(Rad[A-Z]?)-([A-Z]\dC\d{2})_(G\d+)_(s\d{14})_(e\d{14})_(c\d{14}).nc')
    match = regex.match(filename)
    if not match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file name!")
    
    result = aws.get_aws_link_by_filename(filename=filename)

    if(result == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested file does not exists in GOES S3 Bucket!")
    
    
    return {
        'success':True,
        'message':'original bucket link',
        'bucket_link':result
    }