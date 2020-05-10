# MongoDB and Flash Application 
# import dependencies and setup 
from flask_pymongo import PyMongo
from flask import Flask, render_template
# for this one specially import from your scrape_mars.py where you write your scrape function and store the result before we connect it to this flask app.py for us to connect and display it to our index.html
import scrape_mars

# Flask Setup 
app = Flask(__name__)
# Use Flask_pymongo to set up mongo connection on local computer 
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Flask Routes 
# Root Route to Query MongoDB and Pass Mars Data 
@app.route("/")
def home():
    # Pull data from database if anything there
    mars = mongo.db.mars.find_one()
    # Return template and data (why our_data = our_data?)
    return render_template("index.html", mars=mars)

# Route to trigger scrape function 
# take data from our scrape_mars1 
@app.route("/scrape")
def scrape():
    # Run the scrape function pull and store into variable scraped_data
    mars = mongo.db.mars
    scraped_data = mars.scrape_url()
    mars.replace_one({}, scraped_data, upsert=True)
    return "scraped worked"

# Main
if __name__ == "__main__":
    app.run(debug=True)