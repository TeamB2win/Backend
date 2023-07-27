import os

from fastapi import APIRouter, Depends, status, Body
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.http_errors import HTTP_Exception
from app.models.schemas.wanted import VideoPathRequest, VideoPathResponse
from app.db.events import get_db
from app.db.queries.wanted import video_id_exist, video_path_exist, inject_video_path
from app.resources import strings

router = APIRouter(prefix = "/dlserver", tags = ["dlserver"])
api_key_header = APIKeyHeader(name="Token")

InvalidIdException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DSCRIPTION_400_ERROR,
    detail = strings.ID_NOT_FOUD
)

VideoPathExistException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DSCRIPTION_400_ERROR,
    detail = strings.VIDEO_PATH_ALREADY_EXIST
)

VideoPathNotExistException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DSCRIPTION_400_ERROR,
    detail = strings.VIDEO_PATH_NOT_EXIST
)

DataFileNotFoundError = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description = strings.DSCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail = strings.INVAILD_FILE
)


@router.post(
    path = "",
    response_model = VideoPathResponse,
    responses = { **InvalidIdException.responses, 
                 **VideoPathNotExistException.responses, 
                 **DataFileNotFoundError.responses
                 },
    status_code = status.HTTP_200_OK,
    name = "dlserver:register-video-path",
)
async def register_video_path(
    db_session : AsyncSession = Depends(get_db),
    video_request : VideoPathRequest = Body(..., embed = True),
) -> VideoPathResponse :
    if not await video_id_exist(db_session, video_request.id) :
        InvalidIdException.error_raise()
    if not await video_path_exist(db_session, video_request.id) :
        VideoPathNotExistException.error_raise()
    if not os.path.exists(video_request.video) :
        DataFileNotFoundError.error_raise()
    
    await inject_video_path(db_session, video_request)

    return VideoPathResponse(
        **video_request,
        checksum = 'OK'
    )

@router.put(
    path = "",
    response_model = VideoPathResponse,
    responses = { **InvalidIdException.responses, 
                 **VideoPathExistException.responses, 
                 **DataFileNotFoundError.responses
                 },
    status_code = status.HTTP_200_OK,
    name = "dlserver:change-video-source",
)
async def change_video_source(
    db_session : AsyncSession = Depends(get_db),
    video_request : VideoPathRequest = Body(..., embed = True),
) -> VideoPathResponse :
    if not await video_id_exist(db_session, video_request.id) :
        InvalidIdException.error_raise()
    if await video_path_exist(db_session, video_request.id) :
        VideoPathExistException.error_raise()
    if not os.path.exists(video_request.video) :
        DataFileNotFoundError.error_raise()
    
    await inject_video_path(db_session, video_request)