"""
@begin Python_Data_Cleansing_Step2 @desc Python_Data_Cleansing
@in input_from_step1_open_refine @uri file:AirBNBV2.csv
@out output_to_sql_notebook @uri file:02_airbnb_step2_complete.csv
"""


import pandas as pd
import numpy as np
import re


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

"""
@begin get_file
@in input_from_step1_open_refine @uri file:demo_input.csv
@out airbnb_data @AS pd_airbnb_data
"""
def get_file():
    #read file
    file = 'AirBNBV2.csv'  # file after open-refine step
    airbnb_data = pd.read_csv(file, encoding='utf8')
    return airbnb_data
"""
@end get_file
"""

"""
@begin drop_columns_if_exist
@in airbnb_data @AS pd_airbnb_data
@out drop_columns_dataset @as pd_dropped_columns_dataset
"""
def drop_columns_if_exist(airbnb_data):
    dropColumns = ['neighbourhood_group']
    airbnb_data = airbnb_data.drop([x for x in dropColumns if x in airbnb_data.columns], axis=1)

    airbnb_data['host_name 2'] = airbnb_data['host_name 2'].fillna('')

    airbnb_data.set_index('id')
    airbnb_data.head(5)
    return airbnb_data
"""
@end drop_columns_if_exist
"""

"""
@begin mark_nightsLong
@in drop_columns_dataset @as pd_dropped_columns_dataset
@out dataset_marked_nights_long @as pd_marked_nights_long
"""
def mark_nightsLong(airbnb_data):
    # mark where nights were long
    airbnb_data["quality_minimum_nights_long"] = False
    airbnb_data.loc[airbnb_data["minimum_nights"] >= 300, "quality_minimum_nights_long"] = True
    return airbnb_data
"""
@end mark_nightsLong
"""

"""
@begin mark_availability_365
@in drop_columns_dataset @as pd_marked_nights_long
@out dataset_marked_nights_long @as pd_marked_availability
"""
def mark_availability_365(airbnb_data):
    airbnb_data["quality_availability_365"] = False
    airbnb_data.loc[airbnb_data["availability_365"] == 0, "quality_availability_365"] = True
    return airbnb_data

"""
@end mark_availability_365
"""


"""
@begin out_std
@PARAM df
@PARAM column
@out upper_bound @as upper_std
@out lower_bound @as lower_std
"""
def out_std(df, column):
    global lower,upper
    # calculate the mean and standard deviation of the data frame
    data_mean, data_std = df[column].mean(), df[column].std()
    # calculate the cutoff value
    cut_off = data_std * 3
    # calculate the lower and upper bound value
    lower, upper = data_mean - cut_off, data_mean + cut_off
    print('The lower bound value is', lower)
    print('The upper bound value is', upper)
    # Calculate the number of records below and above lower and above bound value respectively
    df1 = df[df[column] > upper]
    df2 = df[df[column] < lower]
    return print('Total number of outliers are', df1.shape[0]+ df2.shape[0])

"""
@end out_std
"""

"""
@begin mark_quality_price_outlier
@in drop_columns_dataset @as pd_marked_availability
@in upper_std @as upper_std
@in lower_std @as lower_std
@out dataset_marked_price_outlier @as pd_marked_price_outlier
"""
def mark_quality_price_outlier(airbnb_data):
    airbnb_data["quality_price_outlier"] = False
    airbnb_data.loc[airbnb_data["price"] > upper, "quality_price_outlier"] = True
    airbnb_data.loc[airbnb_data["price"] < lower, "quality_price_outlier"] = True
    airbnb_data.loc[airbnb_data["price"] == 0, "quality_price_outlier"] = True
    return airbnb_data

"""
@end mark_quality_price_outlier
"""

"""
@begin clean_names
@in marked_price_outlier @as pd_marked_price_outlier
@out dataset_clean_names @as pd_clean_names
"""
def clean_names(airbnb_data):
    airbnb_data.loc[airbnb_data["host_name 1"] == '(Email hidden by Airbnb)', "host_name 1"] = 'Unavailable'
    airbnb_data.loc[airbnb_data["host_name 1"].isnull(), "host_name 1"] = 'Unavailable'
    return airbnb_data
"""
@end clean_names
"""

"""
@begin clean_30_days
@in clean_names @as pd_clean_names
@out dataset_clean_30_days @as pd_clean_30_days
"""
def clean_30_days(airbnb_data):
    airbnb_data.loc[airbnb_data["name"].str.contains('30 Day', case=False), "minimum_nights"] = 30
    return airbnb_data
"""
@end clean_30_days
"""

"""
@begin remove_non_utf8
@in clean_names @as pd_clean_30_days
@out dataset_utf8 @as pd_utf8
"""
def remove_non_utf8(name):
    return re.sub(r'[^\x00-\x7f]', r' ', name)
"""
@end remove_non_utf8
"""

def clean_nonutf8(airbnb_data):
    airbnb_data['name'] = airbnb_data['name'].apply(remove_non_utf8)
    return airbnb_data


"""
@begin remove_special_characters
@in dirty_col @as dirty_col
@out clean_col @as clean_col
"""
def remove_special_characters(df_column,bad_characters_list):
    clean_df_column = df_column
    for bad_char in bad_characters_list:
        clean_df_column = clean_df_column.str.replace(bad_char,' ')
        print("row changes in column " + str(df_column.name) + " after removing character " + str(bad_char) + ": " ,sum(df_column!=clean_df_column))
    clean_df_column = clean_df_column.str.title()
    return clean_df_column

"""
@end remove_special_characters
"""

"""
@begin clean_remove_special_characters
@in pd_utf8 @as pd_utf8
@out dirty_col @as dirty_col
@in clean_col @as clean_col
@out dataset_no_spec_chars @as pd_no_spec_chars
"""
def clean_remove_special_characters(airbnb_data):
    bad_chars_lst = ["*","!","?", "(", ")", "-", "_"]
    airbnb_data['name'] = remove_special_characters(airbnb_data['name'],bad_chars_lst)
    airbnb_data['host_name 1'] = remove_special_characters(airbnb_data['host_name 1'],bad_chars_lst)
    airbnb_data['host_name 2'] = remove_special_characters(airbnb_data['host_name 2'],bad_chars_lst)
    return  airbnb_data
"""
@end clean_remove_special_characters
"""


"""
@begin remove_consecutive_spaces
@in dirty_col @as dirty_col_cons
@out clean_col @as clean_col_cons
"""
def remove_consecutive_spaces(df_column):
    clean_df_column = df_column.replace('\s\s+', ' ', regex=True)
    print("row changes in column " + str(df_column.name) +": " ,sum(df_column!=clean_df_column))
    return clean_df_column
"""
@end remove_consecutive_spaces
"""

"""
@begin clean_consecutive_spaces
@in dataset_no_spec_chars @as pd_no_spec_chars
@out dataset_no_consec_spaces @as pd_no_consec_spaces
@out dirty_col @as dirty_col_cons
@in clean_col @as clean_col_cons
"""
def clean_consecutive_spaces(airbnb_data):
    airbnb_data['name'] = remove_consecutive_spaces(airbnb_data['name'])
    airbnb_data['host_name 1'] = remove_consecutive_spaces(airbnb_data['host_name 1'])
    airbnb_data['host_name 2'] = remove_consecutive_spaces(airbnb_data['host_name 2'])
    airbnb_data['neighbourhood'] = remove_consecutive_spaces(airbnb_data['neighbourhood'])
    airbnb_data['room_type'] = remove_consecutive_spaces(airbnb_data['room_type'])
    return  airbnb_data
"""
@end clean_consecutive_spaces
"""

"""
@begin trim_head_tail_space
@in dirty_col @as dirty_col_trim
@out clean_col @as clean_col_trim
"""
def trim_head_tail_space(df_column):
    clean_df_column = df_column.str.strip()
    print("row changes in column " + str(df_column.name) +": " ,sum(df_column!=clean_df_column))
    return clean_df_column
"""
@end trim_head_tail_space
"""

"""
@begin clean_head_tail_spaces
@in dataset_no_consec_spaces @as pd_no_consec_spaces
@out dataset_trim_spaces @as pd_trim_spaces
@out dirty_col @as dirty_col_trim
@in clean_col @as clean_col_trim
"""
def clean_head_tail_spaces(airbnb_data):
    airbnb_data['name'] = trim_head_tail_space(airbnb_data['name'])
    airbnb_data['host_name 1'] = trim_head_tail_space(airbnb_data['host_name 1'])
    airbnb_data['host_name 2'] = trim_head_tail_space(airbnb_data['host_name 2'])
    airbnb_data['neighbourhood'] = trim_head_tail_space(airbnb_data['neighbourhood'])
    airbnb_data['room_type'] = trim_head_tail_space(airbnb_data['room_type'])
    return airbnb_data
"""
@end clean_head_tail_spaces
"""

"""
@begin clean_empty_names
@in dataset_trim_spaces @as pd_trim_spaces
@out dataset_clean_empty_names @as pd_clean_empty_names
"""
def clean_empty_names(airbnb_data):
    print(airbnb_data['name'].isna().sum())
    airbnb_data['name'] = airbnb_data['name'].fillna('AirBNBListing')
    print(airbnb_data['name'].isna().sum())

    airbnb_data.loc[airbnb_data["name"] == "", "name"] = 'AirBnBListing'
    airbnb_data.loc[airbnb_data["name"] == 'AirBnBListing']
    return airbnb_data
"""
@end clean_empty_names
"""

"""
@begin clean_mark_missing
@in dataset_clean_empty_names @as pd_clean_empty_names
@out dataset_mark_missing @as pd_mark_missing
"""
def clean_mark_missing(airbnb_data):
    ### Create missing indicator for features with missing data
    for col in airbnb_data.columns:
        missing = airbnb_data[col].isnull()
        num_missing = np.sum(missing)
        if num_missing > 0:
            airbnb_data['quality_{}_ismissing'.format(col)] = missing

    ### Based on the indicator, count number of Nan values in each row
    ismissing_cols = [col for col in airbnb_data.columns if 'ismissing' in col]
    airbnb_data['quality_num_missing'] = airbnb_data[ismissing_cols].sum(axis=1)
    return airbnb_data
"""
@end clean_mark_missing
"""

"""
@begin clean_rename_name_columns
@in dataset_mark_missing @as pd_mark_missing
@out dataset_rename_nam_cols @as pd_rename_nam_cols
"""
def clean_rename_name_columns(airbnb_data):
    airbnb_data = airbnb_data.rename(columns={'host_name 1': 'host_name_primary', 'host_name 2': 'host_name_secondary'})
    return airbnb_data
"""
@end clean_rename_name_columns
"""

"""
@begin clean_reviews_per_month
@in dataset_rename_nam_cols @as pd_rename_nam_cols
@out dataset_clean_rev_per_month @as pd_clean_rev_per_month
"""
def clean_reviews_per_month(airbnb_data):
    airbnb_data['reviews_per_month'] = airbnb_data['reviews_per_month'].fillna(value=0)
    return airbnb_data
"""
@end clean_reviews_per_month
"""

"""
@begin output_csv
@in dataset_clean_rev_per_month @as pd_clean_rev_per_month
@out output @as output_to_sql_notebook @uri  file:02_airbnb_step2_complete.csv
"""
def output_csv(airbnb_data):
    airbnb_data.to_csv('02_airbnb_step2_complete.csv', index=False)
"""
@end output_csv
"""

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

"""
@end Python_Data_Cleansing_Step2
"""
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    """ Demo of clean_name_and_date_workflow script """
    print_hi('PyCharm')
    df = get_file()
    df = drop_columns_if_exist(df)
    df = mark_nightsLong(df)
    df = mark_availability_365(df)


    out_std(df, 'price')
    df = mark_quality_price_outlier(df)


    df = clean_names(df)

    df_no_name = df[df["host_name 1"] == 'Unavailable']
    #print(df_no_name.shape)

    df = clean_30_days(df)
    df = clean_nonutf8(df)
    df = clean_remove_special_characters(df)
    df = clean_consecutive_spaces(df)

    df = clean_head_tail_spaces(df)
    df = clean_empty_names(df)
    df = clean_mark_missing(df)

    print(df.shape)
    df = clean_rename_name_columns(df)
    df = clean_reviews_per_month(df)
    
    print(df.shape)
    #output_csv(df)

