from fastapi import APIRouter, Depends
from sensor_service.schemas.metrics import Metric
from sensor_service.business_logic.sensors_logic import SensorDataCollector
from sensor_service.utils.database import AsyncSession, get_db

router = APIRouter()

@router.post("/")
async def collectMetrics(payload: Metric, db: AsyncSession = Depends(get_db)):
    """
    This api route is intended to colect weather data from various sensors and store in the database.
    """
    return await SensorDataCollector.collect_data(payload, db)
