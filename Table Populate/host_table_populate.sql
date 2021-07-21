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