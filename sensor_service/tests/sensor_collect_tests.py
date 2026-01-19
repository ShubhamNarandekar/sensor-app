from datetime import datetime
import pytest
from sensor_service.models.metrics import MetricModel


@pytest.mark.asyncio
async def test_post_api(async_client):   
    response = await async_client.post("/sensors/", json={
                                                    "timestamp": datetime.now().isoformat(),
                                                    "sensor_id": "api_test_sensor",
                                                    "temperature": 34,
                                                    "humidity": 56.0,
                                                    "wind_speed": 10.8})
    assert response.status_code == 200
    data = response.json()
    assert data["sensor_id"] == "api_test_sensor"


@pytest.mark.asyncio
async def test_insert_data(db_session):
    data = MetricModel(timestamp=datetime.now(), 
                           sensor_id="db_test_sensor", 
                           temperature=45, 
                           humidity=23, 
                           wind_speed=6.8)   
    
    db_session.add(data)
    await db_session.commit()
    result = await db_session.get(MetricModel, (data.timestamp, data.sensor_id))
    assert result is not None
    assert result.sensor_id == "db_test_sensor"
    assert result.temperature == 45
    assert result.humidity == 23
    assert result.wind_speed == 6.8
