# solrcli - Solr CLI

Super simple (and small) Command Line Interface to perform frequend actions upon Solr instance. 

Search features are provided from [**pysolr lib**](https://github.com/django-haystack/pysolr/) by [**Django Haystack**](https://github.com/django-haystack).


## Installation

```bash
pip install solrcli
```

## Configuration

Solrcli can take parameters in two ways:

* via a config file
* via command line

Using config file allows you to set up different environments. See example below `hosts.yml`:

```
production-server:
  host: solr-production.foo.com
  core: products
  sanity_checks:
    column_values_at_least: 
      column: enabled

staging-server:
  host: solr-staging.foo.com
  core: products
  sanity_checks:
    column_values_at_least: 
      column: enabled

```

You can choose enviroment in the command line as:

```bash
(venv) $ python -m solrcli -c hosts.ini -i test-server reload
```

If you prefer to provide params each time you can pass `--host` and `--core` as application options before command.


## Usage

### Generic options

Print help informations for main command with `python -m solrcli --help`. Use `--help` after the command to print specific options.

```bash
Usage: solrcli.py [OPTIONS] COMMAND [ARGS]...

Options:
  --host TEXT                 Solr hostname with port
  --core TEXT                 Solr core
  -c, --config TEXT           config file path
  --skipconf / --no-skipconf  ignore configurations
  --help                      Show this message and exit.

Commands:
  fullimport
  getconfig
  query
  reload
  showsettings
  status
```

### Reloading

Invoke core reload

```bash
(venv) $ python -m solrcli --host=my-solr-instance.com --core=core0 reload
```

### Configurations

Get config from Solr instance passing feature from the list below:

* dataimport

```bash
(venv) $ python -m solrcli --host=my-solr-instance.com --core=core0 getconfig --feature=dataimport
```

### Status

Get core status. If you use `--waitfinish` the script will wait until `fullimport` finish.

The `--notify` allows you to receive an email with core counts.

```bash
Usage: solrcli.py status [OPTIONS]

Options:
  --waitfinish / --no-waitfinish  Wait if data import is running
  --notify TEXT                   Comma separated list of e-mail to deliver
                                  result
  --help                          Show this message and exit.
```


### Full import

Invoke core data import handler. 
```bash
Usage: solrcli.py fullimport [OPTIONS]

Options:
  --sanitycheck / --no-sanitycheck
                                  Perform full-import only if sanity check
                                  succeded.
  --notify TEXT                   Comma separated list of e-mail to deliver
                                  result
  --help                          Show this message and exit.
```

The `--notify` params allows you to receive an e-mail after data import will be completed.

If `--sanitycheck` is provided `fullimport` is called only if all sanity checks are passed. 
Sanity checks to be perfomed can be defined in the settings YAML file in the instance like below:

```yaml
instances:
  core-test:
    host: my-solr-instance.com
    core: core0
    sanity_checks:
      column_values_at_least: 
        column: published
```

### Traversing response

This tool can be used to fetch small parts of an arbitrary response. Assume the following snippet is from a `search` request like http://localhost:8973/solr/core0/search/en?rows=0&warehouse=123 

```json
{
    "responseHeader": {
        "status": 0,
        "QTime": 13,
        "params": {}
    },
    "grouped": {
        "country": {
            "matches": 320,
            "ngroups": 212,
            "groups": []
            }
        },
    ...
  "facetes_list": {      
      "facet_fields": {
        "languages": ["EN", 202,
                      "PT", 10],
    ...
}
```

Using _solrcli_ we can get a single information

```bash
$ ./solrcli.py --skipconf query --url="http://localhost:8973/solr/core0/search/en?rows=0&warehouse=123" --find=grouped/contry/ngroups
```

Will return `212` because this value is extracted from the full response traversing nodes.
We can also fetch for childs:

```bash
$ ./solrcli.py --skipconf query --url="http://localhost:8973/solr/core0/search/en?rows=0&warehouse=123" --find=facetes_list/facet_fields/languages
```

obtaining

```
["EN", 202, "PT", 10]
```


## Sanity Checks

We plan to build a set of sanity checks to be performed before full import call to prevent errors or inconsistent data sets.

Currently available sanity checks are:

- `column_values_at_least`: ensure at list `1` or `gt` param value is present in `column`
- `custom_query`: perform a custom query and check if `expected_result` is returned

## TODO

* authentication
* deeper config inspection
* ~focus results: perform a `/search` or similar and get back only interesting nodes~
* query using URL
* v2 Api for Solr Cloud

## Authors

* [**Andrea Carmisciano**](https://github.com/acarmisc/)


## License

This project is licensed under the GNU Affero General Public License v3.0 License - see the [LICENSE](LICENSE) file for details
