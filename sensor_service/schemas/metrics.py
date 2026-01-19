from pydantic import BaseModel, Field
from datetime import datetime

class Metric(BaseModel):
    sensor_id: str
    temperature: float | None
    wind_speed: float | None
    humidity: float | None
    timestamp: datetime = Field(default_factory=datetime.now)


class ResponseData(BaseModel):
    sensor_id: str
    metrics: dict
