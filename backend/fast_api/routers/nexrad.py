from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. schemas import User, Nexrad
from .. oauth2 import get_current_user
from awscloud.s3 import nexrad_main as aws
from .. data.mapdata import MapData
import re

mapData = MapData()

router = APIRouter(
    prefix='/nexrad',
    tags=['NEXRAD 18']
)


@router.get('/files')
def get_all_nexrad_file(stationId: str, year: str, day: str, month: str, response: Response, get_current_user:User = Depends(get_current_user)):
    # Code to retrieve from filename form SQL Lite DB.
    result = aws.get_all_nexrad_file_name_by_filter(station=stationId, year=year, day=day, month=month)

    return {
        'success':True,
        'all_files': result
    }

@router.post('/generate/aws-link', status_code=status.HTTP_201_CREATED)
def generate_aws_link(request: Nexrad, get_current_user:User = Depends(get_current_user)):
    
    result = aws.get_nexrad_aws_link(request.year, request.month, request.day, request.station_id, request.file_name)
    
    if(result == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested file does not exists!")

    team_link, nexrad_link = result

    return {
        'success':True,
        'message':'link generated',
        'team_link':team_link,
        'nexrad_link':nexrad_link
    }



@router.post('/generate/aws-link-by-filename/{filename}', status_code=status.HTTP_201_CREATED)
def generate_aws_link_by_filename(filename, get_current_user:User = Depends(get_current_user)):
    
    regex = re.compile(r'K[A-Z]{3}[0-9]{8}_[0-9]{6}(_V06_MDM)?')
    match = regex.match(filename)

    if not match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file name!")
    
    result = aws.get_nexrad_aws_link_by_filename(filename=filename)

    if(result == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested file does not exists in Nexrad S3 Bucket!")
    
    
    return {
        'success':True,
        'message':'original bucket link',
        'bucket_link':result
    }


@router.get('/map-data', status_code=status.HTTP_200_OK)
def get_map_data(get_current_user:User = Depends(get_current_user)):
    
    return mapData.get_data_for_map()
