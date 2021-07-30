-- dropping tables if they already exist

IF OBJECT_ID('airbnb_base') IS NOT NULL
    DROP TABLE airbnb_base;
GO

IF OBJECT_ID('airbnb_base2') IS NOT NULL
    DROP TABLE airbnb_base2;
GO

IF OBJECT_ID('review_summary') IS NOT NULL
    DROP TABLE review_summary;
GO

IF OBJECT_ID('listing') IS NOT NULL
    DROP TABLE listing;
GO

IF OBJECT_ID('location') IS NOT NULL
    DROP TABLE location;
GO

IF OBJECT_ID('neighbourhood') IS NOT NULL
    DROP TABLE neighbourhood;
GO


IF OBJECT_ID('neighbourhood') IS NOT NULL
    DROP TABLE neighbourhood;
GO

IF OBJECT_ID('host') IS NOT NULL
    DROP TABLE host;
GO

IF OBJECT_ID('airbnb_base') IS NOT NULL
    DROP TABLE airbnb_base;
GO

-- creating a staging table for population of tables with ICs
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

-- create host table with ICs
IF OBJECT_ID('host') IS NOT NULL
    DROP TABLE host;
GO

CREATE TABLE host (
    host_id int ,
    host_name_primary varchar(255) NOT NULL,
	host_name_secondary varchar(255)  NULL,
	calculated_host_listings_count int NOT NULL
    PRIMARY KEY (host_id),
);

INSERT INTO host
select distinct host_id, host_name_primary, host_name_secondary, calculated_host_listings_count from [dbo].[airbnb_base]

-- create neighbourhood with ICs

IF OBJECT_ID('neighbourhood') IS NOT NULL
    DROP TABLE neighbourhood;
GO

CREATE TABLE neighbourhood (
    neighbourhood_id int IDENTITY ,
	neighbourhood varchar(255) NOT NULL,
    PRIMARY KEY (neighbourhood_id),
	CONSTRAINT UC_neighbourhood UNIQUE (neighbourhood )
);

INSERT INTO neighbourhood
select distinct [neighbourhood] from [dbo].[airbnb_base]

-- create location table with ICs
IF OBJECT_ID('location') IS NOT NULL
    DROP TABLE listing;
    DROP TABLE location;
GO

CREATE TABLE location (
    location_id int IDENTITY(1,1),
    latitude decimal(10,8) NOT NULL,
    longitude decimal(10,8) NOT NULL,
	neighbourhood_id int NOT NULL
    PRIMARY KEY (location_id),
	FOREIGN KEY (neighbourhood_id)	REFERENCES neighbourhood(neighbourhood_id),
);



INSERT INTO location
select distinct 
[latitude], [longitude], [neighbourhood].neighbourhood_id
from [dbo].[airbnb_base]
LEFT JOIN [dbo].[neighbourhood] ON [airbnb_base].neighbourhood = [neighbourhood].neighbourhood


-- create room_type table with ICS

IF OBJECT_ID('room_type') IS NOT NULL
    DROP TABLE room_type;
GO

CREATE TABLE room_type (
    room_type_id int identity(1,1) ,
    room_type varchar(255) NOT NULL,
    PRIMARY KEY (room_type_id),
	CONSTRAINT UC_roomtype UNIQUE (room_type )
);

INSERT INTO room_type
select distinct room_type from [dbo].[airbnb_base]

-- create listing table with ICS

IF OBJECT_ID('listing') IS NOT NULL
    DROP TABLE listing;
GO

CREATE TABLE listing (
    listing_id int,
	host_id int, 
    name varchar(255) NOT NULL,
    price money NOT NULL,
	quality_price_outlier bit NOT NULL,
    minimum_nights int NOT NULL, 
	quality_minimum_nights_long bit NOT NULL,
    availability_365 int NOT NULL,
	quality_availability_365 bit NOT NULL,
	location_id int NOT NULL,
	room_type_id int NOT NULL,
    PRIMARY KEY (listing_id),
	FOREIGN KEY (location_id)	REFERENCES location(location_id), 
	FOREIGN KEY (room_type_id)	REFERENCES room_type(room_type_id)

);


INSERT INTO listing
select distinct 
[id],[host_id],[name],[price],[quality_price_outlier], [minimum_nights], quality_minimum_nights_long, [availability_365],quality_availability_365, [location].[location_id], r.room_type_id
from [dbo].[airbnb_base]
LEFT JOIN  [dbo].[location] ON 
([airbnb_base].[latitude] = [dbo].[location].[latitude]  and  [airbnb_base].[longitude] = [dbo].[location].[longitude])
INNER JOIN room_type r ON
[airbnb_base].room_type = r.room_type

IF OBJECT_ID('review_summary') IS NOT NULL
    DROP TABLE review_summary;
GO

-- create review summary table with ICs
CREATE TABLE review_summary (
    review_summary_id int IDENTITY(1,1),
    listing_id int NOT NULL,
    number_of_reviews int NOT NULL,
	last_review date  NULL,
	quality_last_review_ismissing bit NOT NULL, 
	reviews_per_month decimal(5,2),
	quality_reviews_per_month_ismissing bit NOT NULL,
	quality_num_missing int NOT NULL,
    PRIMARY KEY (review_summary_id),
	FOREIGN KEY (listing_id)	REFERENCES listing(listing_id),
);


INSERT INTO review_summary
select distinct 
id, [number_of_reviews], [last_review], quality_last_review_ismissing,  [reviews_per_month], quality_reviews_per_month_ismissing, quality_num_missing
from [dbo].[airbnb_base]


--#final query to pull out information from tables into a view for analysis

select 
l.[listing_id] as id, 
l.[name] as name, 
l.[host_id] as host_id,  
h.[host_name_primary] as host_name_primary, 
h.[host_name_secondary] as host_name_secondary, 
n.[neighbourhood] as neighbourhood,
loc.[location_id], 
loc.[latitude], 
loc.[longitude], 
room.room_type,
l.[price], 
l.[minimum_nights], 
r.[number_of_reviews], 
r.[last_review], 
r.[reviews_per_month],
h.[calculated_host_listings_count],
l.[availability_365], 
l.[quality_minimum_nights_long],
l.quality_availability_365,
l.quality_price_outlier,
r.quality_last_review_ismissing,
r.quality_reviews_per_month_ismissing,
r.quality_num_missing



 --########################
 --report all IC violations, i.e., where at least two rows have the same ID but have different attribute values.
--IC Checks
--no IC violations in the id of the original dataset
select id 
from airbnb_raw
group by id
having count(*) > 1
-- 0 rows, no IC issue


select host_id
from airbnb_raw
group by host_id
having count(*) > 1
--997 rows


select neighbourhood from airbnb_raw
group by neighbourhood
having count(*) > 1
--77 rows

select room_type
from airbnb_raw
group by room_type
having count(*) > 1
--3 rows 

--########################
-- Cleaned data 
--listing table
--report all IC violations, i.e., where at least two rows have the same ID but have different attribute values.
--Checking listing_id
select listing_id
from listing
group by listing_id
having count(*) > 1
--returns 0 rows


select * from listing where host_id = 
(select host_id
from host
group by host_id
having count(*) > 1
)
--returns 0 rows


select * from [dbo].[neighbourhood] where [neighbourhood_id] = 
(select [neighbourhood]
from [neighbourhood]
group by [neighbourhood]
having count(*) > 1
)
-- returns 0 rows

select * from [dbo].[room_type] where [room_type] = 
(
select room_type 
from room_type
group by room_type
having count(*) > 1
)
--returns 0 rows









