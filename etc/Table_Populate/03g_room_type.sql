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