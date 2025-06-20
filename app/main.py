from fastapi import FastAPI

from .api import router_blog, router_project, router_tag, router_user
from .core.config import settings

# def create_tables():
#     from .db.base import Base
#     from .db.session import engine

#     from .models import User, Blogpost, Series, Project, Tag, Tech

#     Base.metadata.create_all(bind=engine)


def include_router(app: FastAPI) -> None:
    app.include_router(router_blog, prefix="/api")
    app.include_router(router_project, prefix="/api")
    app.include_router(router_user, prefix="/api")
    app.include_router(router_tag, prefix="/api")


def start_application() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
    # create_tables()
    include_router(app)
    return app


app = start_application()


@app.get("/")
def read_root() -> dict:
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.APP_VERSION}"}
