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

--note the same location id is reused ---
INSERT INTO listing
select distinct 
[id],[host_id],[name],[price],[quality_price_outlier], [minimum_nights], quality_minimum_nights_long, [availability_365],quality_availability_365, [location].[location_id], r.room_type_id
from [dbo].[airbnb_base]
LEFT JOIN  [dbo].[location] ON 
([airbnb_base].[latitude] = [dbo].[location].[latitude]  and  [airbnb_base].[longitude] = [dbo].[location].[longitude])
INNER JOIN room_type r ON
[airbnb_base].room_type = r.room_type


