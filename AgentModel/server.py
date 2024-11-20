from flask import Flask,jsonify
import json,logging,os
import numpy as np
from ModelCity import CityModel

PORT = 8000
app = Flask(__name__,static_url_path='')

model = CityModel(1)

@app.route('/carData',methods=['GET','POST'])
def getCarData():
    model.step()
    print(model.getCarData())
    return jsonify(model.getCarData())
@app.route('/stoplightData',methods=['GET','POST'])
def getStoplight():
    model.step()
    return jsonify(model.getStopLight())

@app.route('/allData',methods=['GET','POST'])
def getAllData():
    model.step()
    return jsonify(model.getAllData())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
    
