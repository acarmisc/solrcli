from pysolr import Solr
import yaml
import time
import click
import requests
import os
import configparser
from libs.configurations import dataimport_config
from libs import sanity_checks


def perform_sanitychecks(remote, config):
    checks = config.get('sanity_checks')
    db_data = remote.get_config('dataimport-config')
    results = []
    
    for k, v in checks.items():
        # injecting db_data in all params
        v['db_data'] = db_data
        results.append(getattr(sanity_checks, k)(**v))
    
    assert all(results), 'Sanity check fails. Stopping execution'

def handle_parameters(cli, host, core, config):
    instance = '{}-{}'.format(host, core)
    
    assert os.path.isfile(config), 'Config file {} not found.'.format(config)
    with open(config, 'r') as stream:
        try:                
            basic_config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

        if basic_config:    
            try:
                host = basic_config['instances'][instance]['host']
                core = basic_config['instances'][instance]['core']            
            except KeyError as e:
                raise ValueError('Configuration error: {}'.format(e))

            if not host or not core:
                raise ValueError('Configuration error: wrong settings in file {}'.format(config))
      
            return host, core, basic_config, instance

    raise ValueError('Configuration error: missing either config file and command line params')

def send_status_notification(cli, recipients, status):
    core = cli.instance.get('core') 
    host = cli.instance.get('host') 

    subject = 'Status notification about {} core {}'.format(host.replace('http://', ''), core)
    message = 'Actual {} status on {} \n'.format(core, host)
    message += 'Document Number: {} \n'.format(status.get('numDocs'))
    message += 'Index Size: {} \n'.format(status.get('size'))
    message += 'Last modified: {} \n'.format(status.get('lastModified'))

    click.echo('Delivering notification to {}'.format(recipients))    

    assert 'email' in cli.config.keys()

    send_email(cli.config.get('email'), recipients, message, subject)


def send_email(config, recipients, message, subject):    
    import base64
    import smtplib, ssl    
    message = message    
    message = '''\
Subject: {}

{}
'''.format(subject, message)

    mailserver = smtplib.SMTP(config.get('host'), int(config.get('port')))
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login(config.get('user'), config.get('password'))
    mailserver.sendmail(config.get('from'), recipients, message)
    mailserver.quit()


class SolrServer():

    base_url = 'http://{}/solr/{}'

    urls = {
        'reload': 'http://{}/solr/admin/cores?action=RELOAD&core={}',
        'full-import': 'http://{}/solr/{}/dataimport?command=full-import',
        'dataimport-config': 'http://{}/solr/{}/dataimport?command=show-config',
        'status': 'http://{}/solr/admin/cores?action=STATUS&core={}'
    }

    def __init__(self, host, core):
        self.host = host
        self.core = core
        for k, v in SolrServer.urls.items():
            self.urls[k] = v.format(host, core)

        self.q = Solr(SolrServer.base_url.format(host, core))

    def get_config(self, config_name):
        ALLOWED_NAMES = ['dataimport-config']
        assert config_name in ALLOWED_NAMES, 'Invalid config_name {}'.format(config_name)
        # TODO: do it more dynamically, handle different dataimport

        if config_name == 'dataimport-config':
            return dataimport_config(self.urls.get('dataimport-config'))

    def invoke_reload(self):
        url = self.urls.get('reload')
        click.echo('Invoking reload: {}'.format(url))
        r = requests.get(url)
        return r

    def invoke_fullimport(self):
        url = self.urls.get('full-import')
        click.echo('Invoking full import: {}'.format(url))
        r = requests.get(url)
        return r

    def get_status(self, waitfinish):
        url = self.urls.get('status')
        click.echo('Invoking status: {}'.format(url))
        r = requests.get(url)
        response = r.json()
        self.status = response.get('status').get(self.core).get('index')

        while self.is_indexing and waitfinish:
            click.echo('Solr core {} indexing is running... sleeping {} seconds'.format(self.core, 10))
            time.sleep(10)
            self.get_status(waitfinish)
        
        return self.status

    @property
    def is_indexing(self):
        return not self.status.get('current')