import numpy as np
import sqlalchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask,jsonify
import datetime as dt

engine=create_engine("sqlite:///Resources/hawaii.sqlite")
Base=automap_base()
Base.prepare(engine,reflect=True)
measurement = Base.classes.measurement
station = Base.classes.station
session=Session(engine)


app = Flask(__name__)

@app.route("/")
def home():
    return (f"Welcome!<br/>"
            f"Available Routes:<br/>"
            f"/api/precipitation<br/>"
            f"/api/stations<br/>"
            f"/api/temperature<br/>"
            f"/api/YY-MM-DD<br/>"
            f"/api/YY-MM-DD/YY-MM-DD<br/>"
           )
@app.route("/api/precipitation")
def precip():
    date=dt.datetime(2016, 8, 22)
    results=session.query(measurement.date,measurement.prcp).filter(measurement.date>date).order_by(measurement.date).all()
    all_prcp=[]
    for date, prcp in results:
        prcp_dict={}
        prcp_dict['date']=date
        prcp_dict['prcp']=prcp
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)


@app.route("/api/stations")
def stat():
    results=session.query(station.name).order_by(station.name).all()
    all_stations=[]
    for name in results:
        station_dict={}
        station_dict['name']=name
        all_stations.append(station_dict)
    return jsonify(all_stations)

@app.route("/api/temperature")
def temp():
    results=session.query(measurement.date,measurement.tobs).filter(measurement.date>'2016-08-22').order_by(measurement.date).all()
    all_tobs=[]
    for date, tobs in results:
        tobs_dict={}
        tobs_dict['date']=date
        tobs_dict['temperature']=tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route('/api/<start_date>/', defaults={'end_date':'2017-08-23'})
@app.route('/api/<start_date>/<end_date>')
def calc_temps(start_date,end_date):
    results=session.query(func.min(measurement.tobs), func.avg(measurement.tobs),func.max(measurement.tobs)).filter(measurement.date >=start_date).filter(measurement.date <= end_date).all()
    all_tmps=[]
    for tmin,tavg,tmax in results:
        tmps_dict={}
        tmps_dict['Min']=tmin
        tmps_dict['Avg']=tavg
        tmps_dict['Max']=tmax
        all_tmps.append(tmps_dict)
    return jsonify(all_tmps)
        

if __name__ == "__main__":
    app.run(debug=True)
