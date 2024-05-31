from flask import Flask, jsonify
from flask_cors import CORS

from scrape import AAScraper
from aadb import AADB

# Initialize flask app
app = Flask(__name__)

# Apply CORS to make the server accessible by frontend
CORS(app)

# Route which scrapes the website(called by cron @ 10 AM)
@app.route("/scrape", methods=["POST"])
def scrape():
    
    response = {"success": False, "message": "Scrapping failed!"}
    
    print("Scrape called")

    # Scraper instance
    scrapper = AAScraper(website_url="https://sahamati.org.in/fip-aa-mapping/")
    # Doc of the scraped AA data
    aa_doc = scrapper.scrape_aas_website()

    db = AADB()
    
    # Save AA data to DB
    save_res = db.save_aa_doc(aa_doc)

    if save_res:
        response = {"success": True, "message": "Scraped succesfully!"}

    return jsonify(response)

# Route to fetch AA docs(used by frontend)
@app.route("/fetch-aa")
def fetch():

    response = {"success": False, "message": "Fetching docs failed!", "data": None}

    db = AADB()
    # Fetch AA docs
    docs = db.fetch_aa_docs()

    if docs:
        response = {"success": True, "message": "Fetching docs passed!", "data": docs}

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
