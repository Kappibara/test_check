from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware


ALLOWED_ORIGINS = "http://localhost http://localhost:8000 http://127.0.0.1:8000"


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
