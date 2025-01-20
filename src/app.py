from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.api.auth import router as auth_router
from src.api.check import router as check_router
from src.database import db_helper
from src.errors import init_exception_handlers
from src.middlewares import init_middlewares


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def init_routes(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/users", tags=["users"])
    app.include_router(check_router, prefix="/checks", tags=["checks"])


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    init_middlewares(app)
    init_routes(app)
    init_exception_handlers(app)
    add_pagination(app)
    return app