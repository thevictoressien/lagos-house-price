import os
import csv
import pytest
import pandas as pd
import numpy as np
import re
from pandas.testing import assert_frame_equal
from clean_data import clean_data
from house_scrapper import house_scrapper


@pytest.fixture(scope="module")
def csv_path():
    """Fixture that runs house_scrapper and returns the CSV path"""
    house_scrapper()
    path = "lag_house_11.csv"
    yield path
    os.remove(path)


def test_csv_file_created(csv_path):
    assert os.path.exists(csv_path), "CSV file not created"


def test_csv_headers(csv_path):
    expected_headers = ["Description", "Location", "Beds", "Baths", "Toilets", "Price"]
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == expected_headers, f"Unexpected headers in CSV file: {headers}"


def test_csv_data(csv_path):
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header row
        rows = list(reader)
        assert len(rows) > 0, "No data found in CSV file"
        for row in rows:
            assert len(row) == 6, f"Unexpected number of fields in row: {row}"


def test_clean_data():
    # Create a sample input DataFrame
    input_data = {
        "Description": ["4 BEDROOM HOUSE FOR SALE", "3 BEDROOM FLAT / APARTMENT FOR SALE"],
        "Location": ["Ikeja Lagos", "Epe Lagos"],
        "Beds": [4, 3],
        "Baths": [3, 2],
        "Toilets": [5, 4],
        "Price": ["50000000", "3000000/perannum"],
    }
    input_df = pd.DataFrame(input_data)

    # Create a sample expected output DataFrame
    expected_data = {
        "Location": ["Ikeja Lagos", "Epe Lagos"],
        "Beds": [4.0, 3.0],
        "Baths": [3.0, 2.0],
        "Toilets": [5.0, 4.0],
        "Price": [50000000.0, 3000000.0],
        "locale": ["Ikeja", "Epe"],
        "House_Type": ["HOUSE", "APARTMENT"],
    }
    expected_df = pd.DataFrame(expected_data)

    # Clean the input DataFrame
    clean_data(input_df)

    # Read the cleaned DataFrame from file
    cleaned_df = pd.read_csv("cleaned_houses.csv")

    # Check that the cleaned DataFrame is as expected
    assert_frame_equal(cleaned_df, expected_df)
