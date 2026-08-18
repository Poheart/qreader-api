import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from qreader import QReader

from app.routes import router


MODEL_SIZE = os.environ.get("MODEL_SIZE", "s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.qreader = QReader(model_size=MODEL_SIZE)
    yield


app = FastAPI(
    title="QReader API",
    description="QR code scanning API powered by QReader",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)
