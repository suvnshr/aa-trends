from scrape import AAScraper

scraper = AAScraper("https://sahamati.org.in/fip-aa-mapping/")


# Test whether the website we're scraping from has the main table
def test_table_exists():
    table = scraper.soup.find("table", id=AAScraper.AA_TABLE_ID)

    # Whether the table exists?
    assert bool(table) == True


# Test the output structure of the aa_doc to be saved
def test_doc_output_structure():
    aa_doc = scraper.scrape_aas_website()

    # Whether the doc is a valid dict with a valid date property?
    assert type(aa_doc) is dict and type(aa_doc["date"]) is str
