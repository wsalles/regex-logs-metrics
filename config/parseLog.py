# -*- coding: utf-8 -*-
import re
from collections import Counter

class Parse():
    def __init__(self, file):
        # Recebe os dados do arquivo log
        self.file = file

    def searchElement(self, key, regex):
        # Testa se houve retorno do elemento procurado na regex
        try:
            self.element = regex.group(key)
        except:
            self.element = "0"
        return self.element

    def counters(self, list_):
        # Funcao para contar quantas vezes o valor X se repete
        # Ex: {'s3.glbimg.com' : 1000}
        c = Counter(list_)
        d = dict(c)
        return d

    def MinMaxValue(self, sum_, mt):
        # Realiaza o teste a fim de retornar o valor minimo ou maximo da lista
        # Se o segundo arumento 'mt' receber 'max', o teste retornara o valor maximo da lista
        # Se o segundo arumento 'mt' receber 'min', o teste retornara o valor minimo da lista
        m = 0
        for x in range(len(sum_)):
            if mt == 'min':
                if float(sum_[x]) < m:
                    m = float(sum_[x])
            elif mt == 'max':
                if float(sum_[x]) > m:
                    m = float(sum_[x])
        return m

    def getList(self):
        # Metodo utilizado para tratar os campos do arquivo log utilizando expressao regular
        logfile_list = []
        logfile = self.file.split('\n')
        for x in range(len(logfile)):
            if logfile[x]:
                remote_addr = re.search(r'(?P<remote_addr>((([0-9]?[0-9]?[0-9])[.]){3}([0-9]?[0-9]?[0-9]))[ ])',
                                        logfile[x])
                remote_addr = self.searchElement('remote_addr', remote_addr).replace(' ', '')
                time_local = re.search(r'(?P<time_local>([0-9]{2}[/][a-zA-Z]\w*[/][0-9]{4}))', logfile[x])
                time_local = self.searchElement('time_local', time_local)
                host = re.search(r'(?P<host>([a-zA-Z]\w*\.\w*){2})', logfile[x])
                host = self.searchElement('host', host)
                request_ = re.search(r'(?P<request>(?:"[GET|POST|PUT|DEL](.*?)"))', logfile[x])
                request_ = self.searchElement('request', request_).replace('"', '')
                http_referer = re.search(r'(?P<http_referer>(?:"[htps:\/](.*?)"))', logfile[x])
                http_referer = self.searchElement('http_referer', http_referer).replace('"', '')
                http_user_agent = re.search(r'(?P<http_user_agent>(?:"[a-zA-Z][^DEL|GET|PUT|POST|htps](.*?)"))',
                                            logfile[x])
                http_user_agent = self.searchElement('http_user_agent', http_user_agent).replace('"', '')
                http_x_forwarded_for = re.search(r'(?P<http_x_forwarded_for>(?:"[0-9][^DEL|GET|PUT|POST|htps](.*?)"))',
                                                 logfile[x])
                http_x_forwarded_for = self.searchElement('http_x_forwarded_for', http_x_forwarded_for).replace('"', '')
                status = re.search(r'(?P<status>[ ](\d{3})[ ])', logfile[x])
                status = self.searchElement('status', status).replace(' ', '')
                body_bytes_sent = re.search(r'(?P<body_bytes_sent>((\d+)[ ]["]))', logfile[x])
                body_bytes_sent = self.searchElement('body_bytes_sent',
                                                     body_bytes_sent).replace(' ', '').replace('"', '')
                request_time = re.search(r'(?P<request_time>(\[[0-9]?[0-9]?[0-9][.][0-9]?[0-9]?[0-9])\])', logfile[x])
                request_time = self.searchElement('request_time', request_time).replace('[', '').replace(']', '')
                proxy_host = re.search(r'(?P<proxy_host>(\[[a-zA-Z]\S*\]))', logfile[x])
                proxy_host = self.searchElement('proxy_host', proxy_host).replace('[', '').replace(']', '')
                scheme = re.search(r'(?P<scheme>Scheme[: ][ ]\w*)', logfile[x])
                scheme = self.searchElement('scheme', scheme)[7:].replace(' ', '')
                expires = re.search(r'(?P<expires>Expires[: ][ ]\w*)', logfile[x])
                expires = self.searchElement('expires', expires)[8:].replace(' ', '')
                ssl = re.search(r'(?P<ssl>SSL[: ][ ]\w*)', logfile[x])
                ssl = self.searchElement('ssl', ssl)[4:].replace(' ', '')
                #Adiciona todos os valores capturados em uma lista para serem exibidos no final
                logfile_list.append({
                    'remote_addr': remote_addr,
                    'time_local': time_local,
                    'host': host,
                    'request': request_,
                    'status': status,
                    'body_bytes_sent': body_bytes_sent,
                    'http_referer': http_referer,
                    'http_user_agent': http_user_agent,
                    'http_x_forwarded_for': http_x_forwarded_for,
                    'request_time': request_time,
                    'proxy_subrequest': proxy_host,
                    'expires': expires,
                    'scheme': scheme,
                    'ssl': ssl
                })
            else:
                pass  # print('Log not found')
        return logfile_list

    def getMetrics(self, metrics_list):
        # Metodo para juntar informacoes da lista e criar metricas (collections)
        # Collections tem um metodo chamado Counter que realiza a contagem de quantas vezes o valor X foi repetido
        a_r_addr, a_t_local, a_hosts, a_status, a_b_bytes_sent, a_h_user_agent, a_r_time = [], [], [], [], [], [], []
        requests_ = len(metrics_list)
        for y in range(requests_):
            r_addr = metrics_list[y]['remote_addr']
            a_r_addr.append(r_addr)
            t_local = metrics_list[y]['time_local']
            a_t_local.append(t_local)
            hosts = metrics_list[y]['host']
            a_hosts.append(hosts)
            status = metrics_list[y]['status']
            a_status.append(status)
            b_bytes_sent = metrics_list[y]['body_bytes_sent']
            a_b_bytes_sent.append(b_bytes_sent)
            h_user_agent = metrics_list[y]['http_user_agent']
            a_h_user_agent.append(h_user_agent)
            r_time = metrics_list[y]['request_time']
            a_r_time.append(r_time)
        r_addr = self.counters(a_r_addr)
        t_local = self.counters(a_t_local)
        hosts = self.counters(a_hosts)
        status = self.counters(a_status)
        min_bytes_sent = self.MinMaxValue(a_b_bytes_sent, 'min')
        max_bytes_sent = self.MinMaxValue(a_b_bytes_sent, 'max')
        avg_bytes_sent = sum(float(i) for i in a_b_bytes_sent) / len(a_b_bytes_sent)
        h_user_agent = self.counters(a_h_user_agent)
        min_r_time = self.MinMaxValue(a_r_time, 'min')
        max_time = self.MinMaxValue(a_r_time, 'max')
        avg_time = sum(float(i) for i in a_r_time) / len(a_r_time)
        metrics = {
                             'requests': requests_,
                             'remotes_address' : r_addr,
                             'requests_time': {'min': min_r_time, 'avg': avg_time, 'max': max_time},
                             'requests_dates': t_local,
                             'access_hosts': hosts,
                             'http_status_code': status,
                             # 'users_agents': h_user_agent,
                             'bytes_sent': {'min': min_bytes_sent, 'avg': avg_bytes_sent, 'max': max_bytes_sent}
                  }
        return metrics