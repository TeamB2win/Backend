from fastapi import FastAPI

from app.api.endpoint import router

def get_application() -> FastAPI:
    # initialize FastAPI
    application = FastAPI()

    # inject FastAPI router
    application.include_router(router)
    return application

app = get_application()