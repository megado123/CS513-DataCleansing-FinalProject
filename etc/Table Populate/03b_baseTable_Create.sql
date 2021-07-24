IF OBJECT_ID('airbnb_base') IS NOT NULL
    DROP TABLE airbnb_base;
GO

CREATE TABLE airbnb_base (
id VARCHAR(255) NULL,
name VARCHAR(255) NULL,
host_id VARCHAR(255) NULL,
host_name_primary VARCHAR(255) NULL,
host_name_secondary VARCHAR(255) NULL,
neighbourhood VARCHAR(255) NULL,
latitude decimal(10,8),
longitude decimal(10,8),
room_type VARCHAR(255) NULL,
price VARCHAR(255) NULL,
minimum_nights VARCHAR(255) NULL,
number_of_reviews int NULL,
last_review date NULL,
reviews_per_month DECIMAL(5,2) NULL,
calculated_host_listings_count int NULL,
availability_365 VARCHAR(255) NULL,
quality_minimum_nights_long VARCHAR(255) NULL,
quality_availability_365 VARCHAR(255) NULL,
quality_price_outlier VARCHAR(255) NULL,
quality_last_review_ismissing VARCHAR(255) NULL,
quality_reviews_per_month_ismissing VARCHAR(255) NULL,
quality_num_missing VARCHAR(255) NULL
);