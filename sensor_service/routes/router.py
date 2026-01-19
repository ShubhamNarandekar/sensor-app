from fastapi import APIRouter
from sensor_service.routes.metrics import metrics
from sensor_service.routes.sensors import sensors

api_router = APIRouter()
api_router.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])