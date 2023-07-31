import os

from fastapi import APIRouter, Depends, status, Body
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.http_errors import HTTP_Exception
from app.models.schemas.wanted import VideoPathRequest, VideoPathResponse
from app.db.events import get_db
from app.db.queries.wanted import video_id_exist, video_path_exist, inject_video_path
from app.secure.hash import generate_data_hash
from app.resources import strings

router = APIRouter(prefix = "/dl", tags = ["dl"])
api_key_header = APIKeyHeader(name="Token")

InvalidIdException = HTTP_Exception(
    status_code = status.HTTP_404_NOT_FOUND,
    description = strings.DESCRIPTION_404_ERROR,
    detail = strings.ID_NOT_FOUND
)

VideoPathExistException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DESCRIPTION_400_ERROR,
    detail = strings.VIDEO_PATH_ALREADY_EXIST
)

VideoPathNotExistException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DESCRIPTION_400_ERROR,
    detail = strings.VIDEO_PATH_NOT_EXIST
)

DataFileNotFoundError = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DESCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail = strings.INVAILD_FILE
)

@router.post(
    path = "",
    response_model = VideoPathResponse,
    responses = { **InvalidIdException.responses, 
                 **VideoPathExistException.responses, 
                 **DataFileNotFoundError.responses
                 },
    status_code = status.HTTP_201_CREATED,
    name = "dl:register-video-path",
)
async def register_video_path(
    db_session : AsyncSession = Depends(get_db),
    video_request : VideoPathRequest = Body(..., embed = True),
) -> VideoPathResponse :
    if not video_request.is_err :
        if not await video_id_exist(db_session, video_request.id) :
            InvalidIdException.error_raise()
        if await video_path_exist(db_session, video_request.id) :
            VideoPathExistException.error_raise()
        if not os.path.exists(video_request.video) :
            DataFileNotFoundError.error_raise()
    else :
        video_request.video = ""
    await inject_video_path(db_session, video_request)
    await generate_data_hash( db_session )

    return VideoPathResponse(
        id = video_request.id,
        video = video_request.video,
        checksum = 'OK'
    )

@router.put(
    path = "",
    response_model = VideoPathResponse,
    responses = { **InvalidIdException.responses, 
                 **VideoPathNotExistException.responses, 
                 **DataFileNotFoundError.responses
                 },
    status_code = status.HTTP_201_CREATED,
    name = "dl:change-video-source",
)
async def change_video_source(
    db_session : AsyncSession = Depends(get_db),
    video_request : VideoPathRequest = Body(..., embed = True),
) -> VideoPathResponse :
    if not video_request.is_err :
        if not await video_id_exist(db_session, video_request.id) :
            InvalidIdException.error_raise()
        if not await video_path_exist(db_session, video_request.id) :
            VideoPathNotExistException.error_raise()
        if not os.path.exists(video_request.video) :
            DataFileNotFoundError.error_raise()
    else :
        video_request.video = ""
    try :
        await inject_video_path(db_session, video_request)
    finally :
        await db_session.close()

    await generate_data_hash( db_session )

    return VideoPathResponse(
        id = video_request.id,
        video = video_request.video,
        checksum = 'OK'
    )