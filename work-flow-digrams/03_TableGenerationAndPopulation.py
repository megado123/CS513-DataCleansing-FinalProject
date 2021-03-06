"""
@begin SQL_Data_Insertion_Step3 @desc SQL_Data_Cleansing
@in input_from_step2_python @uri file:02_airbnb_step2_complete.csv
@out output_to_sql_notebook @uri file:finaldataset.csv
"""

import pyodbc
import pandas as pd
import numpy as np

"""
@begin get_file
@in input_from_step2_python @uri file:02_airbnb_step2_complete.csv
@out airbnb_data @AS pd_airbnb_data
"""
def get_file():
    file = "02_airbnb_step2_complete.csv"
    df = pd.read_csv(file)
    print('reviews_per_month: ' + str(df['reviews_per_month'].isna().sum()))
    df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
    print('reviews_per_month: ' + str(df['reviews_per_month'].isna().sum()))
    print('--')
    print('number_of_reviews: ' + str(df['number_of_reviews'].isna().sum()))
    df['number_of_reviews'] = df['number_of_reviews'].fillna(0)
    print('number_of_reviews: ' + str(df['number_of_reviews'].isna().sum()))
    print('--')
    print('host_name_secondary: ' + str(df['host_name_secondary'].isna().sum()))
    df['host_name_secondary'] = df['host_name_secondary'].fillna('')
    print('host_name_secondary: ' + str(df['host_name_secondary'].isna().sum()))
    return df
"""
@end get_file
"""

"""
@begin connect_db
@in sql_parameters @as sql_connection_parameters
@out sql_connection @as connection
"""
def connect_db():
    server = 'mmm-adf-optimization.database.windows.net, 1433'
    database = 'airbnb'
    username = 'adfsa'
    password = 'R0ck&R0ll'

    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    return  cnxn
"""
@end connect_db
"""


"""
@begin sql_drop_tables
@in db_connection @as connection
@in drop_table_sql @as sql_drop_table_statement
@out empty_database @as empty_database
"""
def sql_drop_tables(cnxn):
    sql = '''
        IF OBJECT_ID('airbnb_base') IS NOT NULL
            DROP TABLE airbnb_base;

        IF OBJECT_ID('review_summary') IS NOT NULL
            DROP TABLE review_summary;

        IF OBJECT_ID('listing') IS NOT NULL
            DROP TABLE listing;

        IF OBJECT_ID('location') IS NOT NULL
            DROP TABLE location;

        IF OBJECT_ID('neighbourhood') IS NOT NULL
            DROP TABLE neighbourhood;

        IF OBJECT_ID('neighbourhood') IS NOT NULL
            DROP TABLE neighbourhood;

        IF OBJECT_ID('host') IS NOT NULL
            DROP TABLE host;

        IF OBJECT_ID('room_type') IS NOT NULL
            DROP TABLE room_type;
    '''
    cnxn.execute(sql)

    cnxn.commit()
"""
@end sql_drop_tables
"""




"""
@begin sql_create_base_table
@in db_connection @as connection
@in dataset_airbnb_data @as pd_airbnb_data
@in empty_database @as empty_database
@in create_table_sql @as sql_create_base_table_statement
@out sql_basetable @as sql_basetable
"""
def sql_create_base_table(cnxn, df):

    cursor = cnxn.cursor()
    sql = '''
    
    IF OBJECT_ID('airbnb_base') IS NOT NULL
        DROP TABLE airbnb_base;
    
    CREATE TABLE airbnb_base (
    id VARCHAR(255) NULL,
    name VARCHAR(255) NULL,
    host_id VARCHAR(255) NULL,
    host_name_primary VARCHAR(255) NULL,
    host_name_secondary VARCHAR(255) NULL,
    neighbourhood VARCHAR(255) NULL,
    latitude decimal(10,8),
    longitude decimal(10,8),
    room_type VARCHAR(255) NULL,
    price VARCHAR(255) NULL,
    minimum_nights VARCHAR(255) NULL,
    number_of_reviews int NULL,
    last_review date NULL,
    reviews_per_month DECIMAL(5,2) NULL,
    calculated_host_listings_count int NULL,
    availability_365 VARCHAR(255) NULL,
    quality_minimum_nights_long VARCHAR(255) NULL,
    quality_availability_365 VARCHAR(255) NULL,
    quality_price_outlier VARCHAR(255) NULL,
    quality_last_review_ismissing VARCHAR(255) NULL,
    quality_reviews_per_month_ismissing VARCHAR(255) NULL,
    quality_num_missing VARCHAR(255) NULL
    );
    
    
    '''
    cnxn.execute(sql)

    cnxn.commit()

    # Insert Dataframe into SQL Server:
    try:
        for index, row in df.iterrows():
            if pd.isna(row.last_review):
                print('null vlaue for last review')
                print(row.id, row['name'], row.host_id, row.host_name_primary, row.host_name_secondary,
                      row.neighbourhood, row.latitude, row.longitude, row.room_type, row.price, row.minimum_nights,
                      row.number_of_reviews, row.last_review, row.reviews_per_month, row.calculated_host_listings_count,
                      row.availability_365, row.quality_minimum_nights_long, row.quality_availability_365,
                      row.quality_price_outlier, row.quality_last_review_ismissing,
                      row.quality_reviews_per_month_ismissing, row.quality_num_missing)
                cursor.execute(
                    "INSERT INTO dbo.airbnb_base (id, name, host_id, host_name_primary, host_name_secondary,neighbourhood, latitude, longitude, room_type, price,minimum_nights, number_of_reviews, last_review,reviews_per_month, calculated_host_listings_count,availability_365, quality_minimum_nights_long,quality_availability_365, quality_price_outlier,quality_last_review_ismissing, quality_reviews_per_month_ismissing,quality_num_missing) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    row.id, row['name'], row.host_id, row.host_name_primary, row.host_name_secondary, row.neighbourhood,
                    row.latitude, row.longitude, row.room_type, row.price, row.minimum_nights, row.number_of_reviews,
                    None, row.reviews_per_month, row.calculated_host_listings_count, row.availability_365,
                    row.quality_minimum_nights_long, row.quality_availability_365, row.quality_price_outlier,
                    row.quality_last_review_ismissing, row.quality_reviews_per_month_ismissing, row.quality_num_missing)
            else:
                print(row.id, row['name'], row.host_id, row.host_name_primary, row.host_name_secondary,
                      row.neighbourhood, row.latitude, row.longitude, row.room_type, row.price, row.minimum_nights,
                      row.number_of_reviews, row.last_review, row.reviews_per_month, row.calculated_host_listings_count,
                      row.availability_365, row.quality_minimum_nights_long, row.quality_availability_365,
                      row.quality_price_outlier, row.quality_last_review_ismissing,
                      row.quality_reviews_per_month_ismissing, row.quality_num_missing)
                cursor.execute(
                    "INSERT INTO dbo.airbnb_base (id, name, host_id, host_name_primary, host_name_secondary,neighbourhood, latitude, longitude, room_type, price,minimum_nights, number_of_reviews, last_review,reviews_per_month, calculated_host_listings_count,availability_365, quality_minimum_nights_long,quality_availability_365, quality_price_outlier,quality_last_review_ismissing, quality_reviews_per_month_ismissing,quality_num_missing) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    row.id, row['name'], row.host_id, row.host_name_primary, row.host_name_secondary, row.neighbourhood,
                    row.latitude, row.longitude, row.room_type, row.price, row.minimum_nights, row.number_of_reviews,
                    row.last_review, row.reviews_per_month, row.calculated_host_listings_count, row.availability_365,
                    row.quality_minimum_nights_long, row.quality_availability_365, row.quality_price_outlier,
                    row.quality_last_review_ismissing, row.quality_reviews_per_month_ismissing, row.quality_num_missing)
    except Exception as e:
        print(e)
    cnxn.commit()
    cursor.close()

"""
@end sql_create_base_table
"""


"""
@begin populate_host_from_base
@in sql_basetable @as sql_basetable
@in db_connection @as connection
@in create_table_sql @as sql_create_host_table_statement
@out sql_host_table @as sql_host_table
@out uc_host_id @as IC_host_id
"""
def populate_host_from_base(cnx):
    sql = '''
    
    IF OBJECT_ID('host') IS NOT NULL
        DROP TABLE host;
    
    CREATE TABLE host (
        host_id int ,
        host_name_primary varchar(255) NOT NULL,
        host_name_secondary varchar(255)  NULL,
        calculated_host_listings_count int NOT NULL
        PRIMARY KEY (host_id),
    );
    
    INSERT INTO host
    select distinct host_id, host_name_primary, host_name_secondary, calculated_host_listings_count from [dbo].[airbnb_base]
    '''
    cnxn.execute(sql)
    cnxn.commit()

"""
@end populate_host_from_base
"""


"""
@begin populate_neighbourhood_from_base
@in sql_basetable @as sql_basetable
@in db_connection @as connection
@in create_table_sql @as sql_create_neighbourhood_table_statement
@out sql_neighbourhood_table @as sql_neighbourhood_table
@out uc_neighbourhood_id @as IC_neighbourhood_id
@out uc_neighbourhood @as IC_nieghtbourhood
"""
def populate_neighbourhood_from_base(cnxn):
    sql = '''
    IF OBJECT_ID('neighbourhood') IS NOT NULL
        DROP TABLE neighbourhood;

    CREATE TABLE neighbourhood (
        neighbourhood_id int IDENTITY ,
    	neighbourhood varchar(255) NOT NULL,
        PRIMARY KEY (neighbourhood_id),
    	CONSTRAINT UC_neighbourhood UNIQUE (neighbourhood )
    );

    INSERT INTO neighbourhood
    select distinct [neighbourhood] from [dbo].[airbnb_base]
    '''
    cnxn.execute(sql)
    cnxn.commit()
"""
@end populate_neighbourhood_from_base
"""



"""
@begin populate_location_from_base
@in sql_basetable @as sql_basetable
@in db_connection @as connection
@in create_table_sql @as sql_create_location_table_statement
@out sql_location_table @as sql_location_table
@out uc_location_id @as IC_location_id
@in uc_neighbourhood_id @as IC_nieghtbourhood
"""
def populate_location_from_base(cnxn):
    sql = '''
    IF OBJECT_ID('location') IS NOT NULL
        DROP TABLE location;

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

    '''
    cnxn.execute(sql)
    cnxn.commit()

"""
@end populate_location_from_base
"""




"""
@begin populate_room_type_from_base
@in sql_basetable @as sql_basetable
@in db_connection @as connection
@in create_table_sql @as sql_create_room_type_table_statement
@out sql_room_table @as sql_room_type_table
@out uc_room_type_id @as IC_room_type_id
@out uc_room_type @as IC_room_type
"""
def populate_room_type_from_base(cnxn):
    sql = '''
    IF OBJECT_ID('room_type') IS NOT NULL
        DROP TABLE room_type;

    CREATE TABLE room_type (
        room_type_id int identity(1,1) ,
        room_type varchar(255) NOT NULL,
        PRIMARY KEY (room_type_id),
    	CONSTRAINT UC_roomtype UNIQUE (room_type )
    );

    INSERT INTO room_type
    select distinct room_type from [dbo].[airbnb_base]
    '''
    cnxn.execute(sql)
    cnxn.commit()


"""
@end populate_room_type_from_base
"""


"""
@begin populate_listing_from_base
@in sql_basetable @as sql_basetable
@in db_connection @as connection
@in create_table_sql @as sql_create_listing_table_statement
@out sql_listing_table @as sql_listing_table
@out uc_listing_id @as IC_listing_id
@in uc_host_id @as IC_host_id
@in uc_location_id @as IC_location_id
@in uc_room_type_id @as IC_room_type_id
"""
def populate_listing_from_base(cnxn):
    sql = '''
    IF OBJECT_ID('listing') IS NOT NULL
        DROP TABLE listing;

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
    	FOREIGN KEY (host_id) REFERENCES host(host_id),
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
    '''
    cnxn.execute(sql)
    cnxn.commit()

"""
@end populate_listing_from_base
"""





"""
@begin populate_review_summary_from_base
@in sql_basetable @as sql_basetable
@in db_connection @as connection
@in create_table_sql @as sql_create_review_summary_table_statement
@out sql_review_summary_table @as sql_review_summary_table
@out uc_review_summary_id @as IC_review_summary_id
@in uc_listing_id @as IC_listing_id
"""
def populate_review_summary_from_base(cnxn):
    sql = '''
    IF OBJECT_ID('review_summary') IS NOT NULL
        DROP TABLE review_summary;

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

    '''
    cnxn.execute(sql)
    cnxn.commit()

"""
@end populate_review_summary_from_base
"""




"""
@begin retrieve_dataset_from_tables_with_ics
@in db_connection @as connection
@in sql_host_table @as sql_host_table
@in sql_location_table @as sql_location_table
@in sql_listing_table @as sql_listing_table
@in sql_room_type_table @as sql_room_type_table
@in sql_review_summary_table @as sql_review_summary_table
@out output @as output_to_sql_notebook @uri  file:finaldataaset.csv
"""
def retrieve_dataset_from_tables_with_ics(cnxn):
    sql = '''
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
    '''
    sql_query = pd.read_sql_query(sql, cnxn)  # here, the 'conn' is the variable that contains your database connection information from step 2
    df = pd.DataFrame(sql_query)
    df.to_csv('finaldataset.csv', index=False)  # place 'r' before the path name to avoid any errors in the path
"""
@end retrieve_dataset_from_tables_with_ics
"""

"""
@end SQL_Data_Insertion_Step3
"""

if __name__ == '__main__':
    df = get_file()
    cnxn = connect_db()
    #sql_drop_tables(cnxn)
    #sql_create_base_table(cnxn, df) #cursor
    #populate_host_from_base(cnxn)
    #populate_neighbourhood_from_base(cnxn)
    #populate_location_from_base(cnxn)
    #populate_room_type_from_base(cnxn)

    #populate_listing_from_base(cnxn)
    #populate_review_summary_from_base(cnxn)
    retrieve_dataset_from_tables_with_ics(cnxn)