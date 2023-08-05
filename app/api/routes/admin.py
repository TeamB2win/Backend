import os
from datetime import datetime
import secrets

import imageio
from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from app.db.events import get_db
from app.db.queries.admin import (
    create_wanted_data, delete_wanted_data, 
    update_wanted_data, update_wanted_datasource
)
from app.db.queries.wanted import get_wanted_data
from app.db.repositories.wanted import Wanted, WantedDetail, WantedDataSource
from app.models.schemas.admin import (
    CreateVideoDataToDLRequest, CreateWantedDataRequest, UpdateWantedDataRequest,
    CUDWantedDataResponse, DeleteWantedRequest, UpdateWantedMediaRequest
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
    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    description=strings.DESCRIPTION_415_ERROR,
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
    description = strings.DESCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail = strings.DB_DL_PROCESS_NOT_COMPLETED,
    action = image_remove
)
InvaildIDException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DESCRIPTION_400_ERROR,
    detail = strings.ID_NOT_FOUND
)
DBProcessException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DESCRIPTION_400_ERROR,
    detail = strings.DB_PROCESS_NOT_COMPLETED
)

# 데이터 추가
@router.post(
    path = "", 
    status_code=status.HTTP_201_CREATED,
    response_model=CUDWantedDataResponse,
    responses={
        **ImageWriteException.responses,
        **ImageOpenException.responses,
        **ImagePathException.responses,
        **DBRegisterException.responses
    },
    name = "admin:create-wanted-data",
)
async def create_wanted_data_api(
    file: UploadFile = File(...),
    request : CreateWantedDataRequest = Depends(),
    db_session : AsyncSession = Depends(get_db),
) -> CUDWantedDataResponse:
    # Validate image path

    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = os.path.join(os.environ["IMAGE_DIR"], ''.join([current_time, secrets.token_hex(16)]))

    # image write check
    try:
        image_type = file.content_type.split('/')[-1]
        image_path += f".{image_type}"
        print(image_path)
        with open(image_path, 'wb+') as file_object:
            file_object.write(file.file.read())
    except:
        print("Fail to Read the Image bytes")
        ImageWriteException.error_raise( image_path = image_path )
    # imageio read check
    try:
        imageio.imread(image_path) 
    except:
        print("Fail to Open the Image using imageio")
        ImageOpenException.error_raise( image_path = image_path )

    try:
        # Add to wanted Table in B2win DB  
        wanted_data : Wanted = Wanted.create(request=request)
        wanted_data : Wanted = await create_wanted_data(db=db_session, data_table=wanted_data)
        print("insert data into wanted")
        # Add to wanted_detail Table in B2win DB  
        wanted_detail_data : WantedDetail = WantedDetail.create(request=request, id=wanted_data.id)
        wanted_detail_data : WantedDetail = await create_wanted_data(db=db_session, data_table=wanted_detail_data)
        print("insert data into wanted_detail")

        wanted_datasource_data : WantedDataSource = WantedDataSource.create(image_path=image_path, id=wanted_data.id)
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
        DBRegisterException.error_raise( image_path = image_path )
    
    await generate_data_hash( db_session )
    await db_session.close()

    return CUDWantedDataResponse(
        id = wanted_data.id,
        method = 'Create',
        status = 'OK',
    )

async def request_dl_server(data):
    url = os.path.join(os.environ["DL_URL"], "api", "inference")
    print(url)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data=data.json())
        print(response)

    return response

@router.delete(
    path = "",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = CUDWantedDataResponse,
    responses = {
        **InvaildIDException.responses,
        **DBProcessException.responses
    },
    name = "admin:delete-wanted-by-id"
)
async def delete_wanted_data_api(
    request : DeleteWantedRequest,
    db_session : AsyncSession = Depends(get_db),    
) -> CUDWantedDataResponse:
    data = await get_wanted_data( db = db_session, id = request.id )
    if data is None :
        raise InvaildIDException.error_raise()
    try :
        data_sources = await delete_wanted_data( db = db_session, id = request.id )
        for paths in data_sources :
            if os.path.exists(paths) :
                os.remove(paths)
    except :
        await db_session.rollback()
        raise DBProcessException.error_raise()
    await db_session.commit()
    await generate_data_hash( db_session )
    await db_session.close()
    
    return CUDWantedDataResponse(
        id = request.id,
        method = 'Delete',
        status = 'OK'
    )

'''
# 데이터 수정
@router.patch("/app/{criminal_id}", status_code=200)
def update_data(
'''

@router.put(
    path = "/data", 
    status_code=status.HTTP_201_CREATED,
    response_model=CUDWantedDataResponse,
    responses={
        **InvaildIDException.responses,
        **DBRegisterException.responses
    },
    name = "admin:update-wanted-data",
)
async def update_wanted_data_api(
    request : UpdateWantedDataRequest,
    db_session : AsyncSession = Depends(get_db),
) -> CUDWantedDataResponse:
    # Validate image path
    data = await get_wanted_data( db = db_session, id = request.id )
    if data is None :
        raise InvaildIDException.error_raise()
    try:
        # update to wanted Table in B2win DB
        await update_wanted_data(db=db_session, table_type = 'wanted', request = request)
        print("update data into wanted")
        # update to wanted_detail Table in B2win DB  
        await update_wanted_data(db=db_session, table_type = 'wanted_detail',request = request)
        print("update data into wanted_detail")
        # DB 저장 
        await db_session.commit()

    except:
        await db_session.rollback()
        DBProcessException.error_raise()
    
    await generate_data_hash( db_session )
    await db_session.close()

    return CUDWantedDataResponse(
        id = request.id,
        method = 'Update',
        status = 'OK',
    )

@router.put(
    path = "/image", 
    status_code=status.HTTP_201_CREATED,
    response_model=CUDWantedDataResponse,
    responses={
        **ImageWriteException.responses,
        **ImageOpenException.responses,
        **ImagePathException.responses,
        **InvaildIDException.responses,
        **DBRegisterException.responses
    },
    name = "admin:update-wanted-image",
)
async def update_wanted_image_api(
    file: UploadFile = File(...),
    request : UpdateWantedMediaRequest = Depends(),
    db_session : AsyncSession = Depends(get_db),
) -> CUDWantedDataResponse:
    
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    image_path = os.path.join(os.environ["IMAGE_DIR"], ''.join([current_time, secrets.token_hex(16)]))
    # Validate image path
    # image write check
    try:
        image_type = file.content_type.split('/')[-1]
        image_path += f".{image_type}"
        print(image_path)
        with open(image_path, 'wb+') as file_object:
            file_object.write(file.file.read())
    except:
        print("Fail to Read the Image bytes")
        ImageWriteException.error_raise( image_path = image_path )
    # imageio read check
    try:
        imageio.imread(image_path) 
    except:
        print("Fail to Open the Image using imageio")
        ImageOpenException.error_raise( image_path = image_path )

    data : Wanted = await get_wanted_data( db = db_session, id = request.id )
    if data is None :
        raise InvaildIDException.error_raise()
    
    old_image_path = data.datasource[0].image
    try:
        # update to wanted Table in B2win DB
        result = await update_wanted_datasource(db=db_session, id = request.id, image_path = image_path)
        print("update image datasource")
        # DB 저장 
        dl_request = CreateVideoDataToDLRequest(
            id = data.id,
            image_path = image_path,
            wanted_type = data.wanted_type,
            prev_driving_path = None,
            video_path = result.video
        )
        print(dl_request)
        await request_dl_server( data = dl_request )
        await db_session.commit()
    except:
        await db_session.rollback()
        DBRegisterException.error_raise( image_path = image_path )
    if os.path.exists(old_image_path) :
        os.remove(old_image_path)
    await generate_data_hash( db_session )
    await db_session.close()

    return CUDWantedDataResponse(
        id = request.id,
        method = 'Update',
        status = 'OK',
    )

@router.put(
    path = "/video", 
    status_code=status.HTTP_201_CREATED,
    response_model=CUDWantedDataResponse,
    responses={
        **InvaildIDException.responses
    },
    name = "admin:update-wanted-image",
)
async def update_wanted_video_api(
    request : UpdateWantedMediaRequest,
    db_session : AsyncSession = Depends(get_db),
) -> CUDWantedDataResponse:

    data : Wanted = await get_wanted_data( db = db_session, id = request.id )
    if data is None :
        raise InvaildIDException.error_raise()
    
    dl_request = CreateVideoDataToDLRequest(
        id = data.id,
        image_path = data.datasource[0].image,
        wanted_type = data.wanted_type,
        prev_driving_path = data.datasource[0].video,
        video_path = data.datasource[0].driving_video
    )
    print(dl_request)
    await request_dl_server( data = dl_request )

    return CUDWantedDataResponse(
        id = request.id,
        method = 'Update',
        status = 'OK',
    )

