# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
import config.parseLog as pl

__author__ = 'Wallace Salles'
app = Flask(__name__)
api = Api(app)

logs = []
k = []
files = []
show = {}

class Metrics(Resource):
    def get(self):
        for x in range(len(logs)):
            for y in range(len(logs[x])):
                k.append(logs[x][y]['remote_addr'])
        return {'logs': {'remote_addr' : k}}

class List(Resource):
    def get(self):
        return {'logs' : show }

class LogFile(Resource):
    def get(self, file):
        search = next(filter(lambda x: x == file, show), None)
        if search is None:
            return {'logfile': search}, 200 if search else 404
        else:
            return {'logfile' : show[file]}, 200 if show[file] else 404

class Parse(Resource):
    def post(self):
        file = request.files['file']
        self.fname = file.filename
        file = file.read().decode('utf-8')
        logs = pl.Parse(file).getList(self.fname)
        search = next(filter(lambda x: x == self.fname, files), None)
        if search is None:
            files.append(self.fname)
            show[self.fname] = logs #[logs[i] for i in range(len(logs))]
            return show
        return "O arquivo ja foi carregado!"

api.add_resource(Metrics, '/metrics')
api.add_resource(List, '/list')
api.add_resource(LogFile, '/log/<string:file>')
api.add_resource(Parse, '/parse')

app.run(debug=True, host='0.0.0.0', port=80)