--All tables in design leverage primary keys, foreign keys and uniqueness constraints per the ERD diagram.
--These sql queries are to showcase there are no issues with the final table structure per the design

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









