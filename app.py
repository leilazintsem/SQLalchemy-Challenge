import numpy as np
import re
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  

from flask import Flask, jsonify

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
# Flask Routes
#################################################
"""List all available api routes."""
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )
#Convert query results to a dictionary using `date` as the key and `tobs` as the value    
@app.route("/api/v1.0/precipitation") 
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)    

    # Query Measurement
    results = (session.query(Measurement.date, Measurement.tobs)
                      .order_by(Measurement.date))

    # Create a dictionary from the row data and append to a list date and tobs
    date_tobs = []
    for each_row in results:
        dt_dict = {}
        dt_dict["date"] = each_row.date
        dt_dict["tobs"] = each_row.tobs
        date_tobs.append(dt_dict)

    return jsonify(date_tobs)
