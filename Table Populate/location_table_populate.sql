IF OBJECT_ID('location') IS NOT NULL
    DROP TABLE location;
GO

CREATE TABLE location (
    location_id int,
    latitude decimal NOT NULL,
    longitude decimal NOT NULL,
	neighbourhood_id int NOT NULL
    PRIMARY KEY (location_id),
	FOREIGN KEY (neighbourhood_id)	REFERENCES neighbourhood(neighbourhood_id),
);

INSERT INTO location
select distinct 
[id], [latitude], [longitude], [neighbourhood].neighbourhood_id
from [dbo].[airbnb_base]
LEFT JOIN [dbo].[neighbourhood] ON [airbnb_base].neighbourhood = [neighbourhood].neighbourhood


