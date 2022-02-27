import logging

from api.v1 import convertation
from core.config.api import get_config
from db.connections import close_connections, init_connections
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

config = get_config()

app = FastAPI(
    title=config.app_project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    await init_connections()


@app.on_event("shutdown")
async def shutdown():
    await close_connections()


app.include_router(convertation.router, prefix="/api/v1", tags=["convert"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        port=8001,
        log_level=logging.DEBUG,
    )
