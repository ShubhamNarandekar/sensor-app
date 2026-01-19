from datetime import datetime
import json
from pathlib import Path
from sqlalchemy import select, text
from sensor_service.utils.database import AsyncSessionLocal, db_engine
from sensor_service.models.metrics import Base, MetricModel

data_file = Path("sensor_service/sample_data/sample_data.json")

async def load_data_from_json():
    if not data_file.exists():
        print(f"{data_file} not found, skipping load")
        return

    async with db_engine.begin() as conn:
        # Enable TimescaleDB extension (if not exists)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb;"))

        # Create tables from ORM models
        await conn.run_sync(Base.metadata.create_all)

        # Convert table to TimescaleDB hypertable
        await conn.execute(
            text("""
            SELECT create_hypertable(
                'sensor_metrics',
                'timestamp',
                if_not_exists => TRUE
            );
            """)
        )

    async with AsyncSessionLocal() as session:
        # Check if data already exists
        result = await session.execute(select(MetricModel))
        if result.scalars().first() is not None:
            print("Data already exists, skipping JSON load")
            return

        if not data_file.exists():
            print(f"JSON file {data_file} not found, skipping load")
            return

        with open(data_file, "r") as f:
            records = json.load(f)

        sensor_objects = []
        for record in records:
            record_time = datetime.fromisoformat(record["timestamp"].replace("Z", "+00:00"))
            sensor_objects.append(
                MetricModel(
                    timestamp=record_time,
                    sensor_id=record["sensor_id"],
                    temperature=record["temperature"],
                    humidity=record["humidity"],
                    wind_speed=record["wind_speed"]
                )
            )

        session.add_all(sensor_objects)
        await session.commit()
        print(f"Loaded {len(sensor_objects)} rows from JSON")
