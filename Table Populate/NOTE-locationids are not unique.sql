IF OBJECT_ID('review_summary') IS NOT NULL
    DROP TABLE review_summary;

GO

CREATE TABLE review_summary (
    review_summary_id int IDENTITY(1,1),
    listing_id int NOT NULL,
    number_of_reviews int NOT NULL,
	last_review date NOT NULL,
	reviews_per_month DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (review_summary_id),
	FOREIGN KEY (listing_id)	REFERENCES listing(listing_id),
	CONSTRAINT UC_list_id UNIQUE (listing_id )
);

--note the same location id is reused ---
INSERT INTO review_summary
select distinct 
id, number_of_reviews, last_review, reviews_per_month
from [dbo].[airbnb_base]




