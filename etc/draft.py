import re

f = open('../log.txt', 'r')
logfile = f.read().split('\n')

logfile_list = []

print('##### REGEX ######')
for x in range(len(logfile)):
    if logfile[x]:
        remote_addr = re.search(r'(?P<remote_addr>((([0-9]?[0-9]?[0-9])[.]){3}([0-9]?[0-9]?[0-9])))', logfile[x])
        remote_addr = remote_addr.group('remote_addr')
        time_local = re.search(r'(?P<time_local>([0-9]{2}[/][a-zA-Z]\w*[/][0-9]{4}))', logfile[x])
        time_local = time_local.group('time_local')
        host = re.search(r'(?P<host>([a-zA-Z]\w*\.\w*){2})', logfile[x])
        host = host.group('host')
        regex = re.findall(r'(?P<request>(?:"(.*?)"))', logfile[x])
        request = regex[0][0].replace('"', '')
        http_referer = regex[1][0].replace('"', '')
        http_user_agent = regex[2][0].replace('"', '')
        http_x_forwarded_for = regex[3][0].replace('"', '')
        regex = re.findall(r'[ ][0-9]\w*', logfile[x])
        status = regex[0].replace(' ', '')
        body_bytes_sent = regex[1].replace(' ', '')
        regex = re.findall(r'\[(.*?)\]', logfile[x])
        request_time = regex[1].replace('[', '').replace(']', '')
        proxy_host = regex[2].replace('[', '').replace(']', '')
        scheme = re.search(r'(?P<scheme>Scheme[: ][ ]\w*)', logfile[x])
        scheme = scheme.group('scheme')[7:].replace(' ', '')
        expires = re.search(r'(?P<expires>Expires[: ][ ]\w*)', logfile[x])
        expires = expires.group('expires')[8:].replace(' ', '')
        ssl = re.search(r'(?P<ssl>SSL[: ][ ]\w*)', logfile[x])
        ssl = ssl.group('ssl')[4:].replace(' ', '')
        logfile_list.append({
            'remote_addr' : remote_addr,
            'time_local' : time_local,
            'host' : host,
            'request' : request,
            'status' : status,
            'body_bytes_sent' : body_bytes_sent,
            'http_referer' : http_referer,
            'http_user_agent' : http_user_agent,
            'http_x_forwarded_for' : http_x_forwarded_for,
            'request_time' : request_time,
            'proxy_subrequest' : proxy_host,
            'expires' : expires,
            'scheme' : scheme,
            'ssl' : ssl
        })
    else:
        print('Log not found')

print(logfile_list[0])