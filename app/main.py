from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoint import router
from app.config.app import get_app_settings
from app.core.events import create_start_app_handler, create_stop_app_handler


def get_application() -> FastAPI:
    # initialize FastAPI and settings
    application = FastAPI()
    settings = get_app_settings()

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