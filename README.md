# solrcli - Solr CLI

Super simple (and small) Command Line Interface to perform frequend actions upon Solr instance. 

Search features are provided from [**pysolr lib**](https://github.com/django-haystack/pysolr/) by [**Django Haystack**](https://github.com/django-haystack).


## Installation (not yet available)

```bash
pip install solrcli
```

## Configuration

Solrcli can take parameters in two ways:

* via a config file
* via command line

Using config file allows you to set up different environments. See example below `hosts.ini`:

```
[test-server]
host=localhost:8893
core=core0

[production-server]
host=machine.production.priv:80
core=core0
```

You can choose enviroment in the command line as:

```bash
(venv) $ solrcli -c hosts.ini -i test-server reload
```

If you prefer to provide params each time you can pass `--host` and `--core` as application options before command.


## Usage

### Generic options

Print help informations for main command with `solrcli --help`. Use `--help` after the command to print specific options.

```bash
Usage: solrcli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --host TEXT          Solr hostname with port
  --core TEXT          Solr core
  -c, --config TEXT    config file path
  -i, --instance TEXT  remote instance from config file
  --help               Show this message and exit.

Commands:
  fullimport
  getconfig
  reload
```

### Reloading

Invoke core reload

```bash
(venv) $ solrcli --host=my-solr-instance.com --core=core0 reload
```

### Configurations

Get config from Solr instance passing feature from the list below:

* dataimport

```bash
(venv) $ solrcli --host=my-solr-instance.com --core=core0 getconfig --feature=dataimport
```


## TODO

* authentication
* more robust config/parameters handling
* deeper config inspection
* focus results: perform a `/search` or similar and get back only interesting nodes
* query using URL
* v2 Api for Solr Cloud

## Authors

* [**Andrea Carmisciano**](https://github.com/acarmisc/)


## License

This project is licensed under the GNU Affero General Public License v3.0 License - see the [LICENSE](LICENSE.md) file for details