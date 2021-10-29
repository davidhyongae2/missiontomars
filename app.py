from flask import Flask 
from flask import render_template
from flask import redirect
from flask import request
from flask_pymongo import PyMongo
import scraping
from pymongo import MongoClient
import pymongo

# Create an instance of Flask

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    
    mars = mongo.db.mars.find_one()
    
    # Return template and data
    return render_template("index.html", mars = mars)

# Route that will trigger the scrape function    
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars
    data = scraping.scrape_all()
    
    # Update the Mongo Database using update and upsert=True
    mars.update({}, mars_web, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)

# # Given Already
if __name__ == "__main__":
    app.run(debug=True)
