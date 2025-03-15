from fastapi import FastAPI

from core.config import settings
from app.routes import router_blog, router_project, router_user, router_tag


def include_router(app):
    app.include_router(router_blog, prefix="/api")
    app.include_router(router_project, prefix="/api")
    app.include_router(router_user, prefix="/api")
    app.include_router(router_tag, prefix="/api")


def start_application():
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    include_router(app)
    return app


app = start_application()


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.APP_VERSION}"}
