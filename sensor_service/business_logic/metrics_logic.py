from sensor_service.models.metrics import MetricModel
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from sqlalchemy import select, func
from fastapi import HTTPException

class MetricDataRetriever:
    async def sensorData(sensor_ids=None, start_time=None, end_time=None, metrics=None, db=None):
        query = None
        map_columns = {
            "temperature": MetricModel.temperature,
            "humidity": MetricModel.humidity,
            "wind_speed": MetricModel.wind_speed,
        }
        selected_metrics = metrics or list(map_columns.keys())
        aggregates = [func.avg(map_columns[m]).label(m) for m in selected_metrics]

        if sensor_ids:
            query = (select(MetricModel.sensor_id,  
                    *aggregates)
                    .where(MetricModel.sensor_id.in_(sensor_ids))
                    .where(MetricModel.timestamp >= start_time)
                    .where(MetricModel.timestamp <= end_time)
                    .group_by(MetricModel.sensor_id)
                    .order_by(MetricModel.sensor_id))
        else:
            query = (select(MetricModel.sensor_id,
                    *aggregates)
                    .where(MetricModel.timestamp >= start_time)
                    .where(MetricModel.timestamp <= end_time)
                    .group_by(MetricModel.sensor_id)
                    .order_by(MetricModel.sensor_id))
        
        try:
            result = await db.execute(query)
            rows = result.mappings().all()  
            return rows
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Item not found")
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Database error")
        

    async def metricStats(metrics, db):
        map_columns = {
            "temperature": MetricModel.temperature,
            "humidity": MetricModel.humidity,
            "wind_speed": MetricModel.wind_speed,
        }

        try:
            column = map_columns[metrics]
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Provided metric -> {metrics} is not supported")
        
        query = (select(func.min(column).label(f"{metrics}-min"), 
                        func.max(column).label(f"{metrics}-max"),
                        func.avg(column).label(f"{metrics}-average"),
                        func.sum(column).label(f"{metrics}-sum"))
                        .select_from(MetricModel))
        
        try:
            result = await db.execute(query)
            return result.mappings().first()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Database error")



        