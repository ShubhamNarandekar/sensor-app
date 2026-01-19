from datetime import datetime
import pytest
from sensor_service.models.metrics import MetricModel
from sqlalchemy import select, func
from fastapi.encoders import jsonable_encoder

@pytest.mark.asyncio
async def test_data_retrieval(db_session):
    sensor_id = "sensor_1"
    metrics = ["temperature", "humidity"]
    start_time = datetime.fromisoformat("2026-01-15T06:45:00Z")
    end_time = datetime.now()

    map_columns = {
            "temperature": MetricModel.temperature,
            "humidity": MetricModel.humidity,
            "wind_speed": MetricModel.wind_speed,
        }
    selected_metrics = metrics or list(map_columns.keys())
    aggregates = [func.avg(map_columns[m]).label(m) for m in selected_metrics]

    query = (select(MetricModel.sensor_id,  
                    *aggregates)
                    .where(MetricModel.sensor_id == sensor_id)
                    .where(MetricModel.timestamp >= start_time)
                    .where(MetricModel.timestamp <= end_time)
                    .group_by(MetricModel.sensor_id)
                    .order_by(MetricModel.sensor_id))
    result = await db_session.execute(query)
    data = result.first()
    assert data.sensor_id == sensor_id