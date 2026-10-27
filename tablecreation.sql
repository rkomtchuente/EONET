CREATE TABLE natural_events (
    event_id VARCHAR(50) PRIMARY KEY,
    title VARCHAR(255),
    category VARCHAR(100),
    event_date TIMESTAMP,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6)
);