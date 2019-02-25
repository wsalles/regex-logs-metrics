# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from flask_restful import Api, Resource
import config.parseLog as pl
import os

__author__ = 'Wallace Salles'
app = Flask(__name__)
api = Api(app)

# Declara variaveis que serao verificadas e exibidas
logs = []
files = []
show = {}
metrics = {}

@app.route('/')
def index():
    # Pagina com interface usuario para realizar upload do arquivo de log
    return render_template('index.html')

class Metrics(Resource):
    # Classe que retorna as metricas com metodo GET
    def get(self):
        return {'metrics': metrics}

class List(Resource):
    # Classe que retorna lista com todos os dados dos arquivos de logs com metodo GET
    def get(self):
        return {'logs': show}

class LogFile(Resource):
    # Classe que retorna a lista com todos os dados de um arquivo de log especifico com metodo GET
    def get(self, file):
        search = next(filter(lambda x: x == file, show), None)
        if search is None:
            return {'logfile': search}, 200 if search else 404
        else:
            return {'logfile' : show[file]}, 200 if show[file] else 404

class Parse(Resource):
    #Classe responsavel por receber os arquivos de log e processar os dados
    def post(self):
        #Metodo POST que trata o recebimento do arquivo uma unica vez
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
        #Metodo PUT que trata o recebimento do arquivo e atualiza suas informacoes
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

# Declarando os endpoint
api.add_resource(Metrics, '/metrics')
api.add_resource(List, '/list')
api.add_resource(LogFile, '/log/<string:file>')
api.add_resource(Parse, '/parse')

port = int(os.environ.get("PORT", 5000))
app.run(host='0.0.0.0', port=port)