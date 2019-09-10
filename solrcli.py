import requests
import click
from os import sys

from libs.commons import SolrServer, handle_parameters, perform_sanitychecks


@click.group()
@click.option('--host', help='Solr hostname with port')
@click.option('--core', help='Solr core')
@click.option('-c', '--config', help='config file path')
@click.option('-i', '--instance', help='remote instance from config file')
def cli(host, core, config, instance):    
    host, core, config = handle_parameters(cli, host, core, config, instance)
    cli.remote = SolrServer(host, core)
    cli.config = config

@cli.command()
def show_config():    
    print(cli.config)

@cli.command()
def reload():
    r = cli.remote.invoke_reload()
    click.echo('Calling reload: {}'.format(cli.remote.urls.get('reload')))
    print(r.json())


@cli.command()
@click.option('--sanitycheck/--no-sanitycheck', default=False, help='Perform full-import only if sanity check succeded.')
def fullimport(sanitycheck):

    if sanitycheck:
        try:
            perform_sanitychecks(cli.remote, cli.config) #.get_config('dataimport-config'), cli.config.get())
        except AssertionError as e:
            click.echo(e)            
            sys.exit(1)

    c = cli.remote.invoke_fullimport()
    print(c.json())


@cli.command()
@click.option('--feature', help='Which config?', type=click.Choice(['dataimport']), required=True)
def getconfig(feature):
    c = cli.remote.get_config('{}-config'.format(feature))
    print(c)

if __name__ == '__main__':
    cli()
