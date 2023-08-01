from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors.http_errors import HTTP_Exception
from app.db.events import get_db
from app.db.queries.wanted import get_full_wanted_data, get_wanted_data
from app.secure.hash import calculate_hash, get_data_hash, compare_data_hash

from app.models.schemas.wanted import (
    ListOfWantedDataResponse, WantedDataResponse, CheckHashResponse
)
from app.resources import strings

router = APIRouter(prefix = "/wanted", tags = ["wanted"])
HttpError404 = HTTP_Exception(
    status_code = status.HTTP_404_NOT_FOUND,
    description = strings.DESCRIPTION_404_ERROR,
    detail = strings.DATA_NOT_FOUND
)

@router.get(
    path = "",
    response_model = ListOfWantedDataResponse,
    status_code = status.HTTP_200_OK,
    name = "wanted:get-wanted-list",
)
async def list_wanted_for_user(
    db_session: AsyncSession = Depends(get_db),
) -> ListOfWantedDataResponse :
    data = await get_full_wanted_data(db_session)
    data_hash = calculate_hash( data )
    await db_session.close()
    return ListOfWantedDataResponse(
        data_hash = data_hash,
        data = data
    )
    
@router.get(
    path = "/{id}",
    response_model = WantedDataResponse,
    responses = { **HttpError404.responses },
    status_code = status.HTTP_200_OK,
    name = "wanted:get-individual-wanted",
)
async def individual_wanted_for_user(
    id : int = Path(title="The ID of the wanted data to get"),
    db_session: AsyncSession = Depends(get_db),
) -> WantedDataResponse :
    data = await get_wanted_data(db_session, id)
    if not data :
        raise HttpError404.error_raise()
    data_hash = get_data_hash()
    await db_session.close()
    return WantedDataResponse(
        data_hash = data_hash,
        data = [ data ]
    )

@router.get(
    path = "/check/{data_hash}",
    response_model = CheckHashResponse,
    status_code = status.HTTP_200_OK,
    name = "wanted:check-wanted-list",    
)
async def check_wanted_list(
    data_hash : str = Path(title="The data hash of all wanted data to validate"),
) -> CheckHashResponse :
    response = CheckHashResponse(
            data_hash = data_hash
        )
    if not compare_data_hash( 
        required_data_hash = data_hash,
    ) :
        response.status = 'Expired'
    else :
        response.status = 'OK'
    
    return response