from fastapi import APIRouter, status, HTTPException, Response, Depends
from .. schemas import User, Nexrad
from .. oauth2 import get_current_user
from awscloud.s3 import nexrad_main as aws
from .. data.mapdata import MapData

mapData = MapData()

router = APIRouter(
    prefix='/nexrad',
    tags=['NEXRAD 18']
)


@router.get('/files')
def get_all_goes_file(station: str, year: str, day: str, month: str, response: Response, get_current_user:User = Depends(get_current_user)):
    # Code to retrieve from filename form SQL Lite DB.

    return "done"

@router.post('/generate/aws-link', status_code=status.HTTP_201_CREATED)
def generate_aws_link(request: Nexrad, get_current_user:User = Depends(get_current_user)):
    
    team_link, nexrad_link = aws.get_nexrad_aws_link(request.year, request.month, request.day, request.station_id, request.file_name)
    
    return {
        'success':True,
        'message':'link generated',
        'team_link':team_link,
        'nexrad_link':nexrad_link
    }

@router.get('/map-data', status_code=status.HTTP_200_OK)
def get_map_data(get_current_user:User = Depends(get_current_user)):
    
    return mapData.get_data_for_map()
    
    # return {
    #     'success':True,
    #     'message':'link generated',
    #     'team_link':team_link,
    #     'nexrad_link':nexrad_link
    # }