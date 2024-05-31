import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pymongo


class AAScraper:
    
    """ 
    AAScraper provides methods to scrape the website and return data in a doc format
    """
    
    # Constants used while scraping

    # The index after which the AA names start in the table header
    AA_START_INDEX = 4
    
    # The HTML ID of the table to scrape
    AA_TABLE_ID = "tablepress-44"

    def __init__(self, website_url):
        self.website_url = website_url
        self.soup = self.get_soup_instance()

    # get today's date in DD-MM-YYYY format
    def get_date(self):

        today = datetime.today()
        return today.strftime("%d-%m-%Y")

    # Get beautiful soup instance
    def get_soup_instance(self):

        page = requests.get(self.website_url)
        return BeautifulSoup(page.content, "html.parser")

    # Parse the table cells and return status count
    def get_aa_status_count(self, aa_data_tds):

        # Initialize counts
        live_count = 0
        testing_count = 0
        na_count = 0

        # increment the counters, while looping over table cells
        for aa_data in aa_data_tds:
            sanitized_aa_data = aa_data.text.strip()

            if sanitized_aa_data == "Live":
                live_count += 1

            elif sanitized_aa_data == "Testing":
                testing_count += 1

            elif sanitized_aa_data == "x":
                na_count += 1

        return {
            "na_count": na_count,
            "live_count": live_count,
            "testing_count": testing_count,
        }

    # Parse the AA table, and return  AAdata in doc format
    def parse_table(self, table_header, table_body):

        # Get "th" of all AAs
        table_aas = list(table_header.select("th"))[self.AA_START_INDEX :]

        # Intialize AA data
        aa_doc_for_db = {"date": self.get_date(), "aas_data": {}}

        # loop over "th"
        for i, table_aa_th in enumerate(table_aas):
            
            # The AA Name
            aa_name = table_aa_th.text.strip()
            
            # Select all the columns in the table body for that AA
            aa_data_tds = table_body.select(
                "td.column-" + str(i + self.AA_START_INDEX + 1)
            )

            # get the status count that AA
            status_count = self.get_aa_status_count(aa_data_tds)

            # Form the doc with status count data
            aa_doc_for_db["aas_data"][aa_name] = status_count

        return aa_doc_for_db

    # Scrape the AA website
    def scrape_aas_website(self):

        # find the table
        table = self.soup.find("table", id=self.AA_TABLE_ID)
        # Select table header
        table_header = table.select_one("thead > tr")
        
        # Select table body
        table_body = table.select_one("tbody")

        # Parse the table and return the AA data in doc format
        return self.parse_table(table_header, table_body)
