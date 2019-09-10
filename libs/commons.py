from pysolr import Solr
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

def handle_parameters(cli, host, core, config, instance):

    if host and core:
        return host, core        
    elif config and instance:
        assert os.path.isfile(config), 'Config file {} not found.'.format(config)
        import yaml
        with open(config, 'r') as stream:
            try:                
                basic_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                        
        if basic_config:        
            host = basic_config[instance]['host']
            core = basic_config[instance]['core']            

            if not host or not core:
                raise ValueError('Configuration error: wrong settings in file {}'.format(config))
        
            cli.context_settings.update({'config': basic_config})
      
            return host, core, basic_config[instance]

    raise ValueError('Configuration error: missing either config file and command line params')

class SolrServer():

    base_url = 'http://{}/solr/{}'

    urls = {
        'reload': 'http://{}/solr/admin/cores?action=RELOAD&core={}',
        'full-import': 'http://{}/solr/{}/dataimport?command=full-import',
        'dataimport-config': 'http://{}/solr/{}/dataimport?command=show-config'
    }

    def __init__(self, host, core):
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