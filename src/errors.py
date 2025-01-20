from fastapi import FastAPI
from starlette.responses import JSONResponse


class UserAlreadyExistsError(Exception):
    pass

class CheckNotFoundError(Exception):
    pass

class CheckCreationError(Exception):
    pass

class InternalServerError(Exception):
    pass

class UnauthorizedError(Exception):
    pass


async def user_already_exists_exception_handler(request, exc: UserAlreadyExistsError):
    return JSONResponse(
        status_code=400,
        content={"detail": "User already exists"}
    )


async def check_not_found_exception_handler(request, exc: CheckNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "Check not found"}
    )


async def check_creation_exception_handler(request, exc: CheckCreationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Failed to create check"},
    )


async def internal_server_error_exception_handler(request, exc: InternalServerError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"},
    )

async def unauthorized_exception_handler(request, exc: InternalServerError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Incorrect username or password"},
        headers={"WWW-Authenticate": "Bearer"},
    )

def init_exception_handlers(app: FastAPI) -> None:
    app.exception_handler(UserAlreadyExistsError)(user_already_exists_exception_handler)
    app.exception_handler(CheckNotFoundError)(check_not_found_exception_handler)
    app.exception_handler(CheckCreationError)(check_creation_exception_handler)
    app.exception_handler(InternalServerError)(internal_server_error_exception_handler)
    app.exception_handler(UnauthorizedError)(unauthorized_exception_handler)
