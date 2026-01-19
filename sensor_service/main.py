from fastapi import FastAPI
from sensor_service.routes.router import api_router
from contextlib import asynccontextmanager
from sensor_service.sample_data.load_data import load_data_from_json
from sensor_service.utils.database import db_engine
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load sample data on app startup
    await load_data_from_json()
    yield
    # We can do any cleanups at this point

app = FastAPI(
    title="Sensor Data Service",
    version="1.0.0",
    lifespan=lifespan,
    debug=True
)

app.include_router(api_router, prefix="/api/v1")