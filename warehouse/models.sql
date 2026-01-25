CREATE OR REPLACE TABLE gold.fact_taxi_trips AS 
SELECT
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    fare_amount,
    total_amount,
    payment_type,
    DATE(pickup_datetime) as pickup_date,
    EXTRACT(HOUR FROM pickup_datetime) as pickup_hour
FROM silver_nyc_taxi;