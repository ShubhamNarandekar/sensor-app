from sensor_service.schemas.metrics import Metric
from sensor_service.models.metrics import MetricModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from fastapi import HTTPException

class SensorDataCollector():
    async def collect_data(metric: Metric, db):
        data = MetricModel(timestamp=metric.timestamp, 
                           sensor_id=metric.sensor_id, 
                           temperature=metric.temperature, 
                           humidity=metric.humidity, 
                           wind_speed=metric.wind_speed)
        try:
            db.add(data)
            await db.commit()
            await db.refresh(data)
            return data
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=400, detail="Item with this name already exists.")
        except SQLAlchemyError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Database error occurred.")

