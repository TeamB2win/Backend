from fastapi import APIRouter

from app.api.routes.admin import router as admin_router
from app.api.routes.wanted import router as wanted_router

router = APIRouter()

router.include_router(router = admin_router)
router.include_router(router = wanted_router)
