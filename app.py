import numpy as np
from scipy import stats
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&#60start&#62<br/>"
        f"/api/v1.0/&#60start&#62/&#60end&#62"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and prcp"""
    # Query all dates and measurements
    results = session.query(Measurement.date, Measurement.prcp).all()
    mydictionary=dict(results)
    session.close()

    return jsonify(mydictionary)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all Stations"""
    # Query all dates and measurements
    results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
        # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name, latitude, longitude, elevation in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date>=dt.date(2016, 8, 23)).filter(Measurement.station=="USC00519281")
    mylist=list(results)
    session.close()
    return jsonify(mylist)


@app.route("/api/v1.0/<start>")
def startingtemp(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    date_time_obj = dt.datetime.strptime(start, '%Y-%m-%d').date()
    # Query all dates after start
    minresults = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=date_time_obj).all()[0][0]
    averageresults = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=date_time_obj).all()[0][0]
    maxresults=session.query(func.max(Measurement.tobs)).filter(Measurement.date>=date_time_obj).all()[0][0]
    session.close()
    resultsdict = {}
    resultsdict["Average Temperature"] = averageresults
    resultsdict["Minimum Temperature"] = minresults
    resultsdict["Maximum Temperature"] = maxresults

    return jsonify(resultsdict)

@app.route("/api/v1.0/<start>/<end>")
def startingandendingtemp(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    date_time_start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    date_time_end = dt.datetime.strptime(end, '%Y-%m-%d').date()
    # Query all dates after start
    minresults = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=date_time_start).filter(Measurement.date<=date_time_end).all()[0][0]
    averageresults = session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=date_time_start).filter(Measurement.date<=date_time_end).all()[0][0]
    maxresults=session.query(func.max(Measurement.tobs)).filter(Measurement.date>=date_time_start).filter(Measurement.date<=date_time_end).all()[0][0]
    session.close()
    resultsdict = {}
    resultsdict["Average Temperature"] = averageresults
    resultsdict["Minimum Temperature"] = minresults
    resultsdict["Maximum Temperature"] = maxresults

    return jsonify(resultsdict)

if __name__ == '__main__':
    app.run(debug=True)
