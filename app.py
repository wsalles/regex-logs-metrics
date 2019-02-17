# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import config.parseLog as pl

__author__ = 'Wallace Salles'
app = Flask(__name__)
api = Api(app)

logs = []
k = []

class Metrics(Resource):
    def get(self):
        for x in range(len(logs)):
            for y in range(len(logs[x])):
                k.append(logs[x][y]['remote_addr'])
        return {'logs': {'remote_addr' : k}}

class List(Resource):
    def get(self):
        return {'logs': logs}

class Parse(Resource):
    def post(self):
        file = request.files['file']
        file = file.read().decode('utf-8')
        l = pl.Parse(file)
        logs.append(l.getList())
        return logs

api.add_resource(Metrics, '/metrics')
api.add_resource(List, '/list')
api.add_resource(Parse, '/parse')

app.run(debug=True, host='0.0.0.0', port=80)