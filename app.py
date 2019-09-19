from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
#import pymongo
import scrape_mars

app = Flask(__name__)

# creating connection 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)



#conn = 'mongodb://localhost:27017'
#mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_info")
#passing connection to pymongo instance
#client = pymongo.MongoClient(conn)

# connecting to a database will create one if not already available
#mongo = client.mars_db

#mongo.mars_info.drop()

# setting the route
@app.route("/")
def index():
    mars = mongo.db.mars_info.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars_info
    mars_info_data = scrape_mars.scrape()
    mars.update({}, mars_info_data, upsert=True)
    return redirect ("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)