from fastapi import FastAPI

from core.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.APP_VERSION}"}
