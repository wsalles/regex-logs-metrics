# -*- coding: utf-8 -*-
import re

class Parse():
    def __init__(self, file):
        self.file = file

    def searchElement(self, key, regex):
        try:
            self.element = regex.group(key)
        except:
            self.element = ""
        return self.element

    def getList(self, filename):
        logfile = self.file.split('\n')
        logfile_list = []
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
                body_bytes_sent = self.searchElement('body_bytes_sent.group',
                                                     body_bytes_sent.group).replace(' ', '').replace('"', '')
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
        return {'filename' : filename, 'data' : logfile_list}