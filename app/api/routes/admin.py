import os
import io
import datetime, secrets

import asyncio
import imageio
from fastapi import APIRouter, Body, Depends, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.db.events import get_db
from app.db.queries.admin import create_wanted_data
from app.db.repositories.wanted import Wanted, WantedDetail, WantedDataSource
from app.models.schemas.admin import *
from app.secure.hash import generate_data_hash
from app.api.errors.http_errors import HTTP_Exception
from app.resources import strings


router = APIRouter(prefix = "/admin", tags = ["admin"])

ImageWriteException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DSCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail="Can't write the image"
)
ImageOpenException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DSCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail="Can't open image by using image framework(imageio)"
)
ImagePathException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DSCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail="Can't find image path"
)

IMAGE_DIR = '/home/moongni/git/workspace/image'
# Image upload
@router.post(
    path="/uploadimage",
    status_code=status.HTTP_201_CREATED,
    response_model=UploadImageResponse,
    responses={
        **ImageWriteException.responses,
        **ImageOpenException.responses
    }
)
async def upload_image(
    file: UploadFile
) -> UploadImageResponse:
    # get image name
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = os.path.join(IMAGE_DIR, ''.join([current_time, secrets.token_hex(16)]))
    try:
        image_type = file.content_type.split('/')[-1]
        image_path += f".{image_type}"
        with open(image_path, 'wb+') as file_object:
            file_object.write(file.file.read())
    except:
        if os.path.exists(image_path):
            os.remove(image_path)
        print("Fail to Read the Image bytes")
        ImageWriteException.error_raise()

    # check to open Image by paths
    try:
        imageio.imread(image_path) 
    except:
        print("Fail to Open the Image using imageio")
        ImageOpenException.error_raise()

    return UploadImageResponse(
        image_path=image_path,
        status="OK"
    )


# 데이터 추가
@router.post(
    path = "", 
    status_code=status.HTTP_201_CREATED,
    response_model=CreateWantedDataResponse,
    responses={
        **ImagePathException.responses
    }
)
async def create_data(
    request : CreateWantedDataRequest,
    db_session : AsyncSession = Depends(get_db),
) -> CreateWantedDataResponse:
    # Validate image path
    if not os.path.exists(request.image):
        print(f"Invalid Image path {request.image}")
        ImagePathException.error_raise()
    
    try:
        # Add to wanted Table in B2win DB  
        wanted_data : Wanted = Wanted.create(request=request)
        wanted_data : Wanted = await create_wanted_data(db=db_session, data_table=wanted_data)

        # Add to wanted_detail Table in B2win DB  
        wanted_detail_data : WantedDetail = WantedDetail.create(request=request, id=wanted_data.id)
        wanted_detail_data : WantedDetail = await create_wanted_data(db=db_session, data_table=wanted_detail_data)

            
        wanted_datasource_data : WantedDataSource = WantedDataSource.create(image_path=request.image, id=wanted_data.id)
        wanted_datasource_data : WantedDataSource = await create_wanted_data(db=db_session, data_table=wanted_datasource_data)
        print("insert data into table")
    except:
        # TODO: 테이블 내에 데이터가 생성되었다면 삭제 과정 필요
        
        # Image 삭제
        if os.path.exists(request.image):
            os.remove(request.image)
    
    # DL server로 추론 요청
    data = {
        "id": wanted_data.id,
        "wanted_type": wanted_data.wanted_type,
        "image_path": wanted_datasource_data.image,
        "prev_driving_path": wanted_datasource_data.driving_video,
        "video_path": wanted_datasource_data.video
    }
    response = await request_dl_server(data)
    print(response)
                
    data_hash: str = await generate_data_hash( db_session )
    print("data_hash created")
    
    return CreateWantedDataResponse(
        data_hash = data_hash,
        status = 'OK',
    )

async def request_dl_server(data):
    url = "http://63.35.31.27:8080/api/inference"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        print(response)

    return response
'''
# 데이터 수정
@router.patch("/app/{criminal_id}", status_code=200)
def update_data(
'''

# 데이터 삭제
# @router.delete("/app/{criminal_id}", status_code=204)
# def delete_data(
#     criminal_id: int,
#     db_session: AsyncSession = Depends(get_db),
# ):
#     criminal: CriminalData | None = search_criminal_data(session=session, criminal_id=criminal_id)
#     if not criminal:
#         raise HTTPException(status_code=404, detail="ToDo Not Found")

#     delete_criminal_data(session=session, criminal_id=criminal_id)

