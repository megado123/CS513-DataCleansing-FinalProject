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

--note the same location id is reused ---
INSERT INTO location
select distinct 
[latitude], [longitude], [neighbourhood].neighbourhood_id
from [dbo].[airbnb_base]
LEFT JOIN [dbo].[neighbourhood] ON [airbnb_base].neighbourhood = [neighbourhood].neighbourhood


