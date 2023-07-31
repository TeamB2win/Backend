import os
import io
from datetime import datetime
import secrets
import json

import asyncio
import imageio
from fastapi import APIRouter, Body, Depends, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.db.events import get_db
from app.db.queries.admin import create_wanted_data
from app.db.repositories.wanted import Wanted, WantedDetail, WantedDataSource
from app.models.schemas.admin import (
    CreateVideoDataToDLRequest, UploadImageResponse, CreateWantedDataRequest,
    CreateWantedDataResponse,
)
from app.secure.hash import generate_data_hash
from app.api.errors.http_errors import HTTP_Exception, image_remove
from app.resources import strings


router = APIRouter(prefix = "/admin", tags = ["admin"])

ImageWriteException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DESCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail=strings.IMAGE_NOT_WRITABLE,
    action = image_remove
)
ImageOpenException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DESCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail=strings.IMAGE_NOT_OPEN_BY_IMAGEIO,
    action=image_remove
)
ImagePathException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DESCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail=strings.INVAILD_FILE
)
DBRegisterException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description=strings.DESCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail=strings.DB_DL_PROCESS_NOT_COMPLETED,
    action=image_remove
)


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
    image_path = os.path.join(os.environ["IMAGE_DIR"], ''.join([current_time, secrets.token_hex(16)]))
    print(image_path)
    try:
        image_type = file.content_type.split('/')[-1]
        image_path += f".{image_type}"
        with open(image_path, 'wb+') as file_object:
            file_object.write(file.file.read())
    except:
        print("Fail to Read the Image bytes")
        ImageWriteException.error_raise( image_path = image_path )

    # check to open Image by paths
    try:
        imageio.imread(image_path) 
    except:
        print("Fail to Open the Image using imageio")
        ImageOpenException.error_raise( image_path = image_path )

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
        **ImagePathException.responses,
        **DBRegisterException.responses
    },
    name = "admin:create-wanted-data",
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
        print("insert data into wanted")
        # Add to wanted_detail Table in B2win DB  
        wanted_detail_data : WantedDetail = WantedDetail.create(request=request, id=wanted_data.id)
        wanted_detail_data : WantedDetail = await create_wanted_data(db=db_session, data_table=wanted_detail_data)
        print("insert data into wanted_detail")

        wanted_datasource_data : WantedDataSource = WantedDataSource.create(image_path=request.image, id=wanted_data.id)
        wanted_datasource_data : WantedDataSource = await create_wanted_data(db=db_session, data_table=wanted_datasource_data)
        print("insert data into wanted_datasource")

        ## DL 서버 추론 요청
        dl_request = CreateVideoDataToDLRequest(
            id = wanted_data.id,
            image_path = wanted_datasource_data.image,
            wanted_type = wanted_data.wanted_type,
            prev_driving_path = wanted_datasource_data.driving_video,
            video_path = wanted_datasource_data.video
        )
        print(dl_request)
        await request_dl_server( data = dl_request )

        # DB 저장 
        await db_session.commit()

    except:
        await db_session.rollback()
        DBRegisterException.error_raise( image_path = request.image )
    
    finally :
        await db_session.close()
    
    data_hash: str = await generate_data_hash( db_session )

    return CreateWantedDataResponse(
        data_hash = data_hash,
        status = 'OK',
    )

async def request_dl_server(data):
    url = os.path.join(os.environ["DL_URL"], "api", "inference")
    print(url)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data.json())
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

