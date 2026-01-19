# Prerequisites
- Setup the database
- Get the required database docker image
```bash
$ docker pull timescale/timescaledb-ha:pg18
```
- Run the image and specify the **local-path-to-persist-data** and **password**
```bash
$ docker run -d --name timescaledb -p 5432:5432  -v <local-path-to-persist-data>:/var/lib/postgresql/data -e POSTGRES_PASSWORD=<password> timescale/timescaledb-ha:pg18
```
- Save the db url for connection and replace your password in the connection string
```
"postgresql+asyncpg://postgres:<password>@localhost:5432/postgres"
```
- Create a .env file in the root directory and set **DB_CONNECTION** var in it. The file should exists under sensor-app folder.

<br>
<br>
<br>

# Steps to run the app
- Clone the repo
```bash
$ git clone https://github.com/ShubhamNarandekar/sensor-app.git sensor-app
```
- Get into the project folder
```bash
$ cd sensor-app
```
- Create a python environment
```bash
sensor-app$ python3 -m venv .venv
```
- Install required packages
```bash
sensor-app$ pip install -r requirements.txt 
```
- Run the app
```bash
sensor-app$ uvicorn sensor_service.main:app --reload
```
- On app startup, sample data will be loaded into the database. If needed, you can modify the data values in **sensor-app/sample_data/sample_data.json**

<br>
<br>
<br>

# Using the app
- You can use postman to test the functionality of the app.
- Use **http://127.0.0.1:8000/api/v1** as the base url for the app.
- Use **/sensors** endpoint to post sensor data into the app. This endpoint will be used by various sensors to send data. Following are the expected request body fields:
```json
{
 "timestamp": "2026-01-16T07:30:00Z",
 "sensor_id": "sensor_2",
 "temperature": 18.5,
 "humidity": 61.3,
 "wind_speed": 4.2
}
```
- Use **/metrics** endpoint to retrieve weather details. It accepts certain query parameters for filtering of the data:
1. metrics -> List (Required)
2. sensor_ids -> List (Optional)
3. start_time -> datetime (Required)
4. end_time -> datetime (Required)
- Use **/metrics/combined_stats/{metric}** to retrieve statistics for the given metric type. The type should be within supported metric types (temperature, humidity, wind_speed).

<br>
<br>

# Testing
- Tests are implemented using pytest.
- To test api endpoint for POST and db logic run:
```bash
sensor-app$ pytest sensor_service/tests/sensor_collect_tests.py
```
- To test db logic for metric retrieval run:
```bash
sensor-app$ pytest sensor_service/tests/metric_retrieval_tests.py
```



