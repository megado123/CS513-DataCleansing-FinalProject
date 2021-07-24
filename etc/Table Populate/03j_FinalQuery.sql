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


   

from [dbo].[listing] l
INNER JOIN host h on h.host_id = l.host_id
INNER JOIN location loc on loc.[location_id] = l.location_id
INNER JOIN neighbourhood n on n.neighbourhood_id = loc.neighbourhood_id
INNER JOIN review_summary r on r.listing_id = l.listing_id
INNER JOIN room_type room on room.room_type_id = l.room_type_id
order by l.listing_id