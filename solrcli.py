#!/usr/bin/env python

import pprint
import requests
import click
from os import sys

from libs.commons import SolrServer, handle_parameters, perform_sanitychecks, send_status_notification


@click.group()
@click.option('--host', help='Solr hostname with port', default='localhost:8984')
@click.option('--core', help='Solr core')
@click.option('-c', '--config', help='config file path', default='/home/solruser/etl/conf/solrcli.yml')
def cli(host, core, config):   
    try: 
        host, core, config, instance = handle_parameters(cli, host, core, config)
    except ValueError as e:
        click.secho(str(e), fg='red')
        sys.exit(1)

    cli.remote = SolrServer(host, core)
    cli.config = config    
    cli.instance = config['instances'][instance]

@cli.command()
def showsettings():    
    pprint.pprint(cli.instance)

@cli.command()
def reload():
    r = cli.remote.invoke_reload()
    click.echo('Calling reload: {}'.format(cli.remote.urls.get('reload')))
    print(r.json())


@cli.command()
@click.option('--sanitycheck/--no-sanitycheck', default=False, help='Perform full-import only if sanity check succeded.')
@click.option('--notify/--no-notify', default=False, help='whether to send a notification or not')
@click.option('--notify-to', default=None, help='comma separated list of addresses')
def fullimport(sanitycheck, notify, notify_to):

    if sanitycheck:
        try:
            perform_sanitychecks(cli.remote, cli.instance)
        except AssertionError as e:
            click.echo(e)            
            sys.exit(1)

    c = cli.remote.invoke_fullimport()
    
    if notify:
        c = cli.remote.get_status(True)
        notify = notify_to or cli.config.get('email').get('notify_to')
        assert notify, 'No notification address provided'
        send_status_notification(cli, notify.split(','), c)
    else:
        print(c.json())


@cli.command()
@click.option('--feature', help='Which config?', type=click.Choice(['dataimport']), required=True)
def getconfig(feature):
    c = cli.remote.get_config('{}-config'.format(feature))
    print(c)

@cli.command()
@click.option('--waitfinish/--no-waitfinish', default=False, help='Wait if data import is running')
@click.option('--notify', default=False, help="Comma separated list of e-mail to deliver result")
def status(waitfinish, notify):
    c = cli.remote.get_status(waitfinish)
    pprint.pprint(c)

    if notify:
        send_status_notification(cli, notify.split(','), c)
    

if __name__ == '__main__':
    cli()
