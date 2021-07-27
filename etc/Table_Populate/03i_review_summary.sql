IF OBJECT_ID('review_summary') IS NOT NULL
    DROP TABLE review_summary;
GO

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

--note the same location id is reused ---
INSERT INTO review_summary
select distinct 
id, [number_of_reviews], [last_review], quality_last_review_ismissing,  [reviews_per_month], quality_reviews_per_month_ismissing, quality_num_missing
from [dbo].[airbnb_base]


