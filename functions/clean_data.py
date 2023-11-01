import pandas as pd
import numpy as np
import re


lag = pd.read_csv("lag_house.csv")


def clean_data(dataframe):
    """
    Cleans a given pandas DataFrame of real estate data.

    The function removes duplicates, replaces missing values with NaN, removes any rows with missing values,
    removes any whitespace from string columns, converts columns to appropriate data types, converts
    the price column from USD to NGN, creates new columns for location and house type, and drops unnecessary columns.
    The cleaned data is then saved to a new csv file.

    Args:
        dataframe (pandas.DataFrame): The DataFrame to be cleaned.

    Returns:
        None
    """

    # remove any duplicates
    dataframe.drop_duplicates(inplace=True)

    # replace missing values with NaN
    dataframe.replace("", np.nan, inplace=True)

    # remove any rows with missing values
    dataframe.dropna(axis=0, inplace=True)

    # remove any whitespace from string columns
    for col in dataframe.columns:
        if dataframe[col].dtype == "object":
            dataframe[col] = dataframe[col].str.strip()

    # convert columns to appropriate data types
    dataframe["Beds"] = dataframe["Beds"].astype(float)
    dataframe["Baths"] = dataframe["Baths"].astype(float)
    dataframe["Toilets"] = dataframe["Toilets"].astype(float)

    # loops through price column checks for values with dollar signs
    # if they exist split into two, dollar discarded then checked for other
    # special characters then typecast split portion into float and converted
    # to naira by multiplying by rate
    # other part of conditional handles the
    # price rows with no dollar signs
    dataframe["Price"] = [
        float(re.findall("\d+", val.split("$")[1])[0]) * 775
        if "$" in val
        else float(re.findall("\d+", val)[0])
        for val in dataframe.Price
    ]


    # save cleaned data to a new csv file
    dataframe.to_csv("cleaned_houses.csv", index=False)

