"""
house_scrapper.py: a Python script that scrapes house listings data from the website "propertypro.ng" and creates a CSV file with the scraped data.

Usage: 
    python house_scrapper.py

Returns: None, but creates a CSV file with the scraped data in the same directory as the script.

Requirements:
    - Python 3.x
    - requests
    - beautifulsoup4
    - urllib3

Functions:
    house_scrapper(): A function that scrapes house listings data from the website "propertypro.ng" and creates a CSV file with the scraped data.

"""

from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import csv


def house_scrapper():
    """
    A function that scrapes house listings
    data from the website "propertypro.ng"

    Returns:
    None, but creates a CSV file
      with the scraped data.
    """

    # create session for making requests
    session = requests.Session()
    retry = Retry(total=15, connect=15, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # open a csv file for writing
    csv_file = open("lag_house_11.csv", "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["Description","Title", "Location", "Beds", "Baths","Is_new", "Is_furnished", "Is_serviced", "Toilets", "Price"]
    )

    # supply url and headers dictionary
    url = "https://www.propertypro.ng/property-for-sale?search=Lagos&auto=&type=&bedroom=&min_price=&max_price=&page="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
    }

    for page in range(2):
        # make a request to the website and get the content
        try:
            req = requests.get(url + str(page), headers=headers)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            continue

        # initialize a BeautifulSoup object
        soup = BeautifulSoup(req.content, "lxml")

        # find all house listings on the page
        listings = soup.find_all("div", class_="single-room-sale listings-property")
        # loop through each listing and extract relevant data
        for listing in listings:
            if "Land" in listing.find("h3", class_="listings-property-title2").text:
                continue
            else:
                description = (
                    listing.find("h3", class_="listings-property-title2").text
                    )
            if listing.find(class_="listings-property-title") == None:
                continue
            else:
                title = listing.find(class_="listings-property-title").text
            location = (
                listing.find("div", class_="single-room-text")
                .h4.find_next()
                .text.replace('"', "")
            )
            price = (
                listing.find("h3", class_="listings-price")
                .text.replace("â‚¦", "")
                .replace(" ", "")
                .replace(",", "")
                .replace("₦", "")
            )
            beds = listing.find("div", class_="fur-areea").span.text.split(" ")[0]
            baths = (
                listing.find("div", class_="fur-areea")
                .span.find_all_next()[1]
                .text.split(" ")[0]
            )
            toilets = (
                listing.find("div", class_="fur-areea")
                .span.find_all_next()[3]
                .text.split(" ")[0]
            )
            if listing.find("a", href="/property-for-sale/is-new"):
                is_new = 1
            else:
                is_new = 0
            if listing.find("a", href="/property-for-sale/is-furnished"):
                is_furnished = 1
            else:
                is_furnished = 0
            if listing.find("a", href="/property-for-sale/is-serviced"):
                is_serviced = 1
            else:
                is_serviced = 0
            csv_writer.writerow([description, title, location, beds, baths, toilets, is_new, is_furnished, is_serviced, price])

    csv_file.close()


if __name__ == "__main__":
    house_scrapper()
    print("Done.")
