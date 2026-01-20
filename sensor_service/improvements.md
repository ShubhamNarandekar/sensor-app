# Improvements to be done in future

Due to time constraints, I would like to conclude this work as just a proof of concept. I will include some points that I can think can be improved going ahead.

- Sensor data that we are receiving can also include **location** as one of the field so that weeather insights can be driven based on locations.
- I reliazed it until now that we have to return latest data if no start and end dates and provided. In this current work, as of now, start and end dates are mandatory.
- For input validation, I have just validated the **sensor_id** field. But, in future more robust validation can be done for temperature, humidity and wind_speed to have logical values.
- In the sample data, the values that I have provided are very random, so please don't consider them as logical.
- We can have separate table for just storing all the data related to sensors and then use sensor_id as foreign key in the sensor_metrics table. As of now, I am not storing any sensor related data anyhwere.
- For testing, I have not covered all the endpoints and database logic. This can be done later on. Just covered a couple of the important ones.