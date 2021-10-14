from numpy.lib.function_base import average
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

session = Session(engine)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipiation():
    filtered_dates_prcp = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date >= '2016-08-23').group_by(Measurement.date).all()

    session.close()

    prcp = []
    for date, prcp in filtered_dates_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp.append(prcp_dict)

    return jsonify(prcp)



@app.route("/api/v1.0/stations")
def stations():
    available_stations = session.query(Station.name, Station.station)

    session.close()

    stations = []
    for name, station in available_stations:
        stations_dict = {}
        stations_dict["name"] = name
        stations_dict["station"] = station
        stations.append(stations_dict)
    
    return jsonify(stations)



@app.route("/api/v1.0/tobs")
def tobs():
    filtered_dates_tobs = session.query (Measurement.station, Measurement.tobs).\
        filter(Measurement.date > '2016-08-23').\
        filter(Measurement.station == 'USC00519281').\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    tobs_year = []
    for station, tobs in filtered_dates_tobs:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["tobs"] = tobs
        tobs_year.append(tobs_dict)

    return jsonify(tobs_year)



@app.route("/api/v1.0/<start>")
def temp_start(start):
    start = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).all()

    session.close()

    temp_start=[]
    for min, ave, max in start:
        start_dict = {}
        start_dict["Minimum Temperature"] = min
        start_dict["Average"] = average
        start_dict["Maxiumum Temperature"]= max
        temp_start.append(start_dict)
        
    return jsonify(temp_start)
    


@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    start_end = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()

    session.close()
    
    temp_start_end=[]
    for min, ave, max in start_end:
        start_end_dict = {}
        start_end_dict["Minimum Temperature"] = min
        start_end_dict["Average"] = average
        start_end_dict["Maxiumum Temperature"]= max
        temp_start_end.append(start_end_dict)
        
    return jsonify(temp_start_end)


if __name__ == '__main__':
    app.run(debug=True)