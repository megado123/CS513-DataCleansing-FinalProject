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