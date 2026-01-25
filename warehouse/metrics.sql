CREATE OR REPLACE TABLE gold.daily_trip_volume AS
SELECT
    pickup_date,
    COUNT(*) as trip_count,
    SUM(total_amount) as total_revenue
FROM gold.fact_taxi_trips
GROUP BY pickup_date;

CREATE OR REPLACE TABLE gold.hourly_demand as
SELECT
    pickup_hour,
    COUNT(*) as trips,
FROM gold.fact_taxi_trips
GROUP BY pickup_hour;