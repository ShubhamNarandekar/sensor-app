from datetime import datetime
from fastapi import APIRouter, Query, Depends
from sensor_service.business_logic.metrics_logic import MetricDataRetriever
from sensor_service.utils.database import AsyncSession, get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/")
async def getSensors(sensor_ids: list[str] = Query(None, description="Get sensor data from one or more sensors"),
                     start_time: datetime = Query(None, description="Start date from which you want the data to be"),
                     end_time: datetime = Query(None, description="End date till which you want the data to be"),
                     metrics: list[str] = Query(..., description="Type of metric to retrieve"),
                     db: AsyncSession = Depends(get_db)):
    """
    This api route is intended to return metric data based on the sensor details as specified in the requirements.
    """
    data = await MetricDataRetriever.sensorData(sensor_ids, start_time, end_time, metrics, db)
    return jsonable_encoder(data)

@router.get("/combined_stats/{metric}")
async def getMetricsStats(metric: str, db: AsyncSession = Depends(get_db)):
    """
    This api route is intended to return the statistics of the given metrics as specified in the requirements.
    """
    data = await MetricDataRetriever.metricStats(metric, db)
    return jsonable_encoder(data)

# As the /combined_stats api gives the average as well so no need to have separate api for average
# @router.get("/{metric}")
# async def getMetrics(metric: list[str]):
#     data = MetricDataRetriever.metricAverage(metric)
#     return data