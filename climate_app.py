# Dependencies

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session
session = Session(engine)

# Flask setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():

    return(

        f"Available Routes: <br><br>"
        f"/api/v1.0/precipitation<br><br>"
        f"/api/v1.0/stations<br><br>"
        f"/api/v1.0/tobs<br><br>"
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"(Dates range from 2010-01-01 to 2017-08-23). <br><br>"     
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"(Dates range from 2010-01-01 to 2017-08-23). <br><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Query precipitation
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
        all()

    prcp_data = [results]

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():

     # Query stations
    results = session.query(Station.name, Station.station).all()

    station_data = []
    for result in results:
        station_dic = {}
        station_dic['name'] = result[0]
        station_dic['station'] = result[1]
        station_data.append(station_dic)
        
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    
    # Query temperatures
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= "2016-08-24", Measurement.date <= "2017-08-23").\
        all()

    tobs_data = []
    for result in results:
        tobs_dic = {}
        tobs_dic["Date"] = result[0]
        tobs_dic["Temperature"] = int(result[1])
        tobs_data.append(tobs_dic)

    return jsonify(tobs_data)

@app.route('/api/v1.0/<date>/')
def any_date(date):
    
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= date).all()

    data_list = []
    for result in results:
        data_dic = {}
        data_dic['Average Temperature'] = float(result[0])
        data_dic['Highest Temperature'] = float(result[1])
        data_dic['Lowest Temperature'] = float(result[2])
        data_list.append(data_dic)

    return jsonify(data_list)

@app.route('/api/v1.0/<start>/<end>/')
def date_range(start, end):

    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).all()

    date_range = []
    for result in results:
        date_dic= {}
        date_dic["Start Date"] = start
        date_dic["End Date"] = end
        date_dic["Average Temperature"] = float(result[0])
        date_dic["Highest Temperature"] = float(result[1])
        date_dic["Lowest Temperature"] = float(result[2])
        date_range.append(date_dic)
        
    return jsonify(date_range)


if __name__ == '__main__':
    app.run(debug=True)