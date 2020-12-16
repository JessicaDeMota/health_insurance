# 
# IMPORTS
# 
# you might have to import additional things you need
import requests,json
from flask import Flask, render_template, jsonify

from flask_sqlalchemy import SQLAlchemy

#
# SETUP/CONFIG
#
# change the classname to reflect the name of your table
# change the columns to reflect the columns you need
# each row of your data will be an instance of this class

app = Flask(__name__)

app.config["ENV"] = 'development'
app.config["SECRET_KEY"]=b'_5#y2L"F4Q8z\n\xec]/'

# change the following .db file name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///world_insurance.db'
# this line is to prevent SQLAlchemy from throwing a warning
# if you don't get one with out it, feel free to remove
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#
# DB SETUP
# 

# this set's up our db connection to our flask application
db = SQLAlchemy(app)

# this is our model (aka table)
class WorldInsurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # this becomes an integer b/c the output of my data is an integer
    rank = db.Column(db.Integer, nullable=False)
    #this becomes a string because the output of countries are all a sting 
    country = db.Column(db.String(255), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    government = db.Column(db.Integer, nullable=False)
    primary_private = db.Column(db.Integer, nullable=False)
    
#
# VIEWS 
#


# set up your index view to show your "home" page
# it should include:
# links to any pages you have
# information about your data
# information about how to access your data
# you can choose to output data on this page
@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/health/', methods=['GET'])
def health():
    response = requests.get("https://agile-mesa-34252.herokuapp.com/api")
    print(response.status_code)
    j = response.json()
    #print(j)
    return render_template('health.html' , data = j )

# include other views that return html here:
@app.route('/about/')
def about():
    return render_template('about.html')

# set up the following views to allow users to make
# GET requests to get your data in json
# POST requests to store/update some data
# DELETE requests to delete some data

# change this to return your data
@app.route('/api', methods=['GET'])
def get_data():
    table = WorldInsurance.query.all()
    d = []
    for row in table:
        rows_as_dict = {
            "rank" : row.rank,
            "country" : row.country,
            "total" : row.total,
            "government" : row.government,
            "primary_private" : row.primary_private,
        }
        d.append(rows_as_dict)
    return jsonify(d)


# CODE TO BE EXECUTED WHEN RAN AS SCRIPT
#

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
