from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Metric(BaseModel):
    sensor_id: str
    temperature: float | None
    wind_speed: float | None
    humidity: float | None
    timestamp: datetime = Field(default_factory=datetime.now)

    # Validating the sensor_id field to have a fixed prefix for sensor ids
    @field_validator("sensor_id")
    @classmethod
    def validate_sensor_id(cls, input: str):
        if not input.startswith("sensor_"):
            raise ValueError('sensor_id must start with "sensor_"')
        return input
