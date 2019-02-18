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
metrics = []
a_r_addr, a_t_local, a_hosts, a_status, a_b_bytes_sent, a_h_user_agent, a_r_time = [], [], [], [], [], [], []

class Metrics(Resource):
    def counters(self, list_):
        c = Counter(list_)
        d = dict(c)
        return d

    def get(self):
        if len(files) == 0:
            return {'metrics': '{}'}
        else:
            for x in range(len(show)):
                f = files[x]
                requests_ = len(show[f]['data'])
                for y in range(requests_):
                    r_addr = show[f]['data'][y]['remote_addr']
                    a_r_addr.append(r_addr)
                    t_local = show[f]['data'][y]['time_local']
                    a_t_local.append(t_local)
                    hosts = show[f]['data'][y]['host']
                    a_hosts.append(hosts)
                    status = show[f]['data'][y]['status']
                    a_status.append(status)
                    b_bytes_sent = show[f]['data'][y]['body_bytes_sent']
                    a_b_bytes_sent.append(b_bytes_sent)
                    h_user_agent = show[f]['data'][y]['http_user_agent']
                    a_h_user_agent.append(h_user_agent)
                    r_time = show[f]['data'][y]['request_time']
                    a_r_time.append(r_time)
                r_addr = self.counters(a_r_addr)
                t_local = self.counters(a_t_local)
                hosts = self.counters(a_hosts)
                status = self.counters(a_status)
                min_bytes_sent = min(a_b_bytes_sent)
                max_bytes_sent = max(a_b_bytes_sent)
                avg_bytes_sent = sum(a_b_bytes_sent) / len(a_b_bytes_sent)
                h_user_agent = self.counters(a_h_user_agent)
                min_r_time = min(a_r_time)
                max_time = max(a_r_time)
                avg_time = sum(a_r_time) / len(a_r_time)
                metrics.append({})

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
            show[self.fname] = logs
            return show
        return "O arquivo ja foi carregado!"

api.add_resource(Metrics, '/metrics')
api.add_resource(List, '/list')
api.add_resource(LogFile, '/log/<string:file>')
api.add_resource(Parse, '/parse')

app.run(debug=True, host='0.0.0.0', port=80)