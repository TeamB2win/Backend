import os
import hashlib

import cv2
import imageio
import numpy as np
from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.events import get_db
from app.db.queries.admin import create_wanted_data
from app.db.repositories.wanted import Wanted, WantedDetail, WantedDataSource
from app.models.schemas.admin import CreateWantedDataRequest, CreateWantedDataResponse
from app.secure.hash import generate_data_hash
from app.api.errors.http_errors import HTTP_Exception
from app.resources import strings

router = APIRouter(prefix = "/admin", tags = ["admin"])

ImageSaveException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DSCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail="Invalid Image Bytes"
)
ImageOpenException = HTTP_Exception(
    status_code=status.HTTP_400_BAD_REQUEST,
    description=strings.DSCRIPTION_400_ERROR_FOR_DATA_FILE,
    detail="Can't open image by using image framework"
)

# 데이터 추가
@router.post(
    path = "", 
    status_code=status.HTTP_201_CREATED,
    response_model=CreateWantedDataResponse,
    responses={
        **ImageSaveException.responses
    }
)
async def create_data(
    request : CreateWantedDataRequest = Body(..., embed = True),
    db_session : AsyncSession = Depends(get_db),
) -> CreateWantedDataResponse:
    # Add to wanted Table in B2win DB  
    wanted_data : Wanted = Wanted.create(request=request)
    wanted_data : Wanted = await create_wanted_data(db=db_session, data_table=wanted_data)

    # Add to wanted_detail Table in B2win DB  
    wanted_detail_data : WantedDetail = WantedDetail.create(request=request, id=wanted_data.id)
    wanted_detail_data : WantedDetail = await create_wanted_data(db=db_session, data_table=wanted_detail_data)

    # get image name
    m = hashlib.sha256(f"source_{wanted_data.id}".encode('utf-8'))    
    image_path = os.path.join("/workspace/data", m.hexdigest() + '.png')
    # decode bytes to image
    try:
        encoded_img = np.fromstring(request.image, dtype=np.uint8)
        img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
        cv2.imwrite(image_path, img)
    except:
        ImageSaveException.error_raise()
    
    # check to open Image by paths
    try:
        cv2.imread(image_path)
        imageio.imread(image_path) 
    except:
        ImageOpenException.error_raise()
        
    wanted_datasource_data : WantedDataSource = WantedDataSource.create(image_path=image_path, id=wanted_data.id)
    wanted_datasource_data : WantedDataSource = await create_wanted_data(db=db_session, data_table=wanted_datasource_data)

    data_hash : str = await generate_data_hash( db_session )

    return CreateWantedDataResponse(
        data_hash = data_hash,
        status = 'OK',
    )

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

