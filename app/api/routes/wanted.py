from fastapi import APIRouter, HTTPException, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.events import get_db
from app.db.queries.wanted import get_full_wanted_data, get_wanted_data
from app.secure.hash import get_data_hash, compare_data_hash
from app.models.domain.wanted import WantedFullData
from app.models.schemas.wanted import ListOfWantedDataResponse, WantedDataResponse, OptionalListOfWantedDataResponse

router = APIRouter(prefix = "/wanted", tags = ["wanted"])

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
    data_hash = get_data_hash(data)
    return ListOfWantedDataResponse(
        data_hash = data_hash,
        data = data
    )
    
@router.get(
    path = "/{id}",
    response_model = WantedDataResponse,
    status_code = status.HTTP_200_OK,
    name = "wanted:get-individual-wanted",
)
async def individual_wanted_for_user(
    id : int = Path(title="The ID of the wanted data to get"),
    db_session: AsyncSession = Depends(get_db),
) -> WantedDataResponse :
    data = await get_wanted_data(db_session, id)
    data_hash = get_data_hash(data)
    return WantedDataResponse(
        data_hash = data_hash,
        data = data
    )

@router.get(
    path = "/check/{data_hash}",
    response_model = OptionalListOfWantedDataResponse,
    status_code = status.HTTP_200_OK,
    name = "wanted:check-wanted-list",    
)
async def check_wanted_list(
    data_hash : str = Path(title="The data hash of all wanted data to validate"),
    db_session: AsyncSession = Depends(get_db),
) -> OptionalListOfWantedDataResponse :
    wanted_datalist = await get_full_wanted_data(db_session)
    orig_data_hash = get_data_hash(wanted_datalist)

    response = OptionalListOfWantedDataResponse(
            data_hash = orig_data_hash
        )
    if not compare_data_hash(orig_data_hash, data_hash) :
        response.data = wanted_datalist
        response.status = 'NEW_DATA'
    else :
        response.data = [ WantedFullData() ]
        response.status = 'OK'

    return response