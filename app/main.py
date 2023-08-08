from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoint import router
from app.config.app import get_app_settings
from app.core.events import create_start_app_handler, create_stop_app_handler

settings = get_app_settings()

def get_application() -> FastAPI:
    global settings
    # initialize FastAPI and settings
    application = FastAPI(docs_url = settings.docs_url, redoc_url = settings.redoc_url)
    
    # setting midware for cross-domain situation (react.js, For example)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
 
    # set db event handler
    application.add_event_handler(
        "startup",
        create_start_app_handler(application, settings),
    )
    application.add_event_handler(
        "shutdown",
        create_stop_app_handler(application),
    )

    # inject FastAPI router
    application.include_router(router)

    return application

app = get_application()