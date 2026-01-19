from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Text , Float , TIMESTAMP, Index

Base = declarative_base()

class MetricModel(Base):
    __tablename__ = "sensor_metrics"

    timestamp = Column(TIMESTAMP(timezone=True), primary_key=True, nullable=False)
    sensor_id = Column(Text, primary_key=True, nullable=False)
    temperature = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    __table_args__ = (
        Index("idx_sensor_time", "sensor_id", "timestamp"),
    )