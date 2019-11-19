import xmltodict
import requests
import re

    
def dataimport_config(url):
    r = requests.get(url)

    dd = xmltodict.parse(r.text)
    query = dd.get('dataConfig').get('document').get('entity').get('@query')
    db_data = {}


    # TODO: stop assuming jdbc mysql driver
    url = dd.get('dataConfig').get('dataSource').get('@url')
    url_parts = url.split(':')
    url_parts = dict(host=url_parts[2].replace('//', ''), port=url_parts[3].split('/')[0], dbname=url_parts[3].split('/')[1])
    db_data['host'] = url_parts.get('host')
    db_data['port'] = url_parts.get('port')
    db_data['dbname'] = url_parts.get('dbname')
    db_data['username'] = dd.get('dataConfig').get('dataSource').get('@user')
    db_data['password'] = dd.get('dataConfig').get('dataSource').get('@password')
    db_data['query'] = re.sub(' +', ' ', query)

    return db_data