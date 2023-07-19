
from fastapi import APIRouter
from app.api.routes import *

router = APIRouter()

# router 추가 형식
# router.include_router( router_path, tags = ["router_tag"], prefix = "/router_prefix")