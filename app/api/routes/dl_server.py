import os

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.http_errors import HTTP_Exception
from app.db.events import get_db
from app.db.queries.wanted import video_id_exist, video_path_exist, inject_video_path
from app.models.schemas.wanted import VideoPathRequest, VideoPathResponse
from app.resources import strings
from app.secure.hash import generate_data_hash


router = APIRouter(prefix = "/dl", tags = ["dl"])

DBRegisterException = HTTP_Exception(
    status_code = status.HTTP_400_BAD_REQUEST,
    description=strings.DESCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail=strings.DB_DL_PROCESS_NOT_COMPLETED
)
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
    responses = { 
        **InvalidIdException.responses, 
        **VideoPathExistException.responses, 
        **DataFileNotFoundError.responses
    },
    status_code = status.HTTP_201_CREATED,
    name = "dl:register-video-path",
)
async def register_video_path(
    video_request : VideoPathRequest,
    db_session : AsyncSession = Depends(get_db),
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

    try :
        await inject_video_path(db_session, video_request)
    except :
        DBRegisterException.error_raise()
    finally :
        await db_session.close()

    await generate_data_hash( db_session )
    await db_session.close()

    return VideoPathResponse(
        id = video_request.id,
        video = video_request.video,
        checksum = 'OK'
    )


@router.put(
    path = "",
    response_model = VideoPathResponse,
    responses = { 
        **InvalidIdException.responses, 
        **VideoPathNotExistException.responses, 
        **DataFileNotFoundError.responses,
        **DBRegisterException.responses
    },
    status_code = status.HTTP_201_CREATED,
    name = "dl:change-video-source",
)
async def change_video_source(
    video_request : VideoPathRequest,
    db_session : AsyncSession = Depends(get_db),
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
    except :
        DBRegisterException.error_raise()
    finally :
        await db_session.close()

    await generate_data_hash( db_session )
    await db_session.close()
    
    return VideoPathResponse(
        id = video_request.id,
        video = video_request.video,
        checksum = 'OK'
    )