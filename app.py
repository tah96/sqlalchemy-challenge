import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import pandas as pd
import datetime as dt

from flask import Flask, jsonify

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
date_1 = dt.datetime(2016, 8, 23)


@app.route("/")
def home():
    return (
        f"Welcome to my SQL-Alchemy Challenge API</br>"
        f"Below are endpoints to APIs:</br>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start/<start></br>"
        f"/api/v1.0/start/<start>/end/<end></br>"
        f"----------------------------</br>"
        f"When inputing start or end dates please use YYYY-M-D</br>"
        f"If in any other format, an error will return."
    )

@app.route("/api/v1.0/precipitation")
def precipiation():
    session = Session(engine)

    sel = [Measurement.date, Measurement.prcp]
    twelvemonths = session.query(*sel).filter(Measurement.date >= date_1).all()

    session.close()

    twelve_months =[]

    for Measurement.date, Measurement.prcp in twelvemonths:
        twelve_dict = {}
        twelve_dict["date"] = Measurement.date
        twelve_dict["prcp"] = Measurement.prcp
        twelve_months.append(twelve_dict)

    return jsonify(twelve_months)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    sel_2 = [Measurement.station, Station.name, func.count(Measurement.date)]
    station_join = session.query(*sel_2).filter(Measurement.station == Station.station)
    observ_desc =station_join.group_by(Measurement.station)\
            .order_by(func.count(Measurement.date).desc()).all()
    
    session.close()

    observ_list = []

    for Measurement.station, Station.name, count in observ_desc:
        observ_dict = {}
        observ_dict["Station ID"] = Measurement.station
        observ_dict["Name"] = Station.name
        observ_dict["Observation Count"] = count
        observ_list.append(observ_dict)

    return jsonify(observ_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    sel_2 = [Measurement.station, Station.name, func.count(Measurement.date)]
    station_join = session.query(*sel_2).filter(Measurement.station == Station.station)
    first_station = station_join.group_by(Measurement.station)\
            .order_by(func.count(Measurement.date).desc()).first()
    station_1= first_station[0]

    sel_4 = [Measurement.station, Measurement.tobs]
    station_join_3 = session.query(*sel_4).filter(Measurement.station == Station.station).filter(Measurement.date>=date_1)
    station_join_31 =station_join_3.filter(Measurement.station == station_1).all()

    session.close()

    tobs_list = []

    for station, tobs in station_join_31:
        tobs_dict = {}
        tobs_dict["Station ID"] = station
        tobs_dict["TOBS"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/start/<start>")
def start_date(start):

    date_2 = dt.datetime.strptime(start, '%Y-%m-%d')

    session = Session(engine)

    sel_2 = [Measurement.station, Station.name, func.count(Measurement.date)]
    station_join = session.query(*sel_2).filter(Measurement.station == Station.station)
    first_station = station_join.group_by(Measurement.station)\
            .order_by(func.count(Measurement.date).desc()).first()
    station_1= first_station[0]
    
    sel_3 = [Measurement.station, Station.name, Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    station_join_2 = session.query(*sel_3).filter(Measurement.station == Station.station).filter(Measurement.date>=date_2)
    station_filter = station_join_2.filter(Measurement.station == station_1).first()

    lowest_temp = station_filter[3]
    highest_temp = station_filter[4]
    average_temp = station_filter[5]

    session.close()

    temp_list_s = []
    temp_dict_s = {}
    temp_dict_s["TMIN"] = lowest_temp
    temp_dict_s["TMAX"] = highest_temp
    temp_dict_s["TAVG"] = average_temp
    temp_list_s.append(temp_dict_s)

    return jsonify(temp_list_s)

@app.route("/api/v1.0/start/<start>/end/<end>")
def start_end_date(start, end):

    date_3 = dt.datetime.strptime(start, '%Y-%m-%d')
    date_4 = dt.datetime.strptime(end, '%Y-%m-%d' )

    session = Session(engine)

    sel_2 = [Measurement.station, Station.name, func.count(Measurement.date)]
    station_join = session.query(*sel_2).filter(Measurement.station == Station.station)
    first_station = station_join.group_by(Measurement.station)\
            .order_by(func.count(Measurement.date).desc()).first()
    station_1= first_station[0]
    
    sel_3 = [Measurement.station, Station.name, Measurement.date, func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)]
    station_join_2 = session.query(*sel_3).filter(Measurement.station == Station.station).filter(Measurement.date>=date_3).filter(Measurement.date<=date_4)
    station_filter = station_join_2.filter(Measurement.station == station_1).first()

    lowest_temp = station_filter[3]
    highest_temp = station_filter[4]
    average_temp = station_filter[5]

    session.close()

    temp_list_s = []
    temp_dict_s = {}
    temp_dict_s["TMIN"] = lowest_temp
    temp_dict_s["TMAX"] = highest_temp
    temp_dict_s["TAVG"] = average_temp
    temp_list_s.append(temp_dict_s)

    return jsonify(temp_list_s)

if __name__ == '__main__':
    app.run(debug=True)