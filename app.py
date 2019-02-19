# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Api, Resource
import config.parseLog as pl
from collections import Counter

__author__ = 'Wallace Salles'
app = Flask(__name__)
api = Api(app)

logs = []
files = []
show = {}
metrics = {}

class Metrics(Resource):
    def get(self):
        return {'metrics': metrics}

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
        search = next(filter(lambda x: x == self.fname, files), None)
        if search is None:
            file = file.read().decode('utf-8')
            lists = pl.Parse(file).getList()
            files.append(self.fname)
            show[self.fname] = {'filename': self.fname, 'data': lists}
            metrics[self.fname] = pl.Parse(file).getMetrics(lists)
            return show, 201
        return "O arquivo ja foi carregado!"

    def put(self):
        file = request.files['file']
        self.fname = file.filename
        file = file.read().decode('utf-8')
        lists = pl.Parse(file).getList()
        search = next(filter(lambda x: x == self.fname, files), None)
        if search is None:
            files.append(self.fname)
            show[self.fname] = {'filename': self.fname, 'data': lists}
            metrics[self.fname] = pl.Parse(file).getMetrics(lists)
        else:
            show[self.fname] = {}
            metrics[self.fname] = {}
            show[self.fname] = {'filename': self.fname, 'data': lists}
            metrics[self.fname] = pl.Parse(file).getMetrics(lists)
        return show, 201

api.add_resource(Metrics, '/metrics')
api.add_resource(List, '/list')
api.add_resource(LogFile, '/log/<string:file>')
api.add_resource(Parse, '/parse')

app.run(debug=True, host='0.0.0.0', port=80)