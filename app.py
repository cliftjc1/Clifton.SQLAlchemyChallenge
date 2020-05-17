# Import Flask, jsonify
from flask import Flask, jsonify
# Import other dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################

# Create an app, being sure to pass __name__
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Welcome to my 'Home' page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"    ## I'm pretty unsure about these last two bits..
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session from Python to the DB
    session = Session(engine)
    """Return the precipitation data as JSON"""
    #Query all precipitation data
    results = session.query(Measurement.prcp).all()
    session.close()
    #Convert list of tuples into normal list
    precipitation = list(np.ravel(results))

    return jsonify(precipitation)
# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.


@app.route("/api/v1.0/stations")
def stations():
    #Create session from Python to the DB
    session = Session(engine)
    """Return the list of stations from the dataset as JSON"""
    #Query all station data
    results = session.query(Station.station).all()
    #results = session.query(Station.station).group_by(Station.station).all()
    session.close()
    #Convert list of tuples into normal list
    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    #Query the dates and temperature observations of the most active station for the last year of data.
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').filter(Measurement.date > query_date).order_by(Measurement.date).all()
    session.close()
    #Convert list of tuples into normal list
    tobs = list(np.ravel(results))

    return jsonify(tobs)