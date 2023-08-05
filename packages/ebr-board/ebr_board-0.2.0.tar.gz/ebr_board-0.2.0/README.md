# ebr-board

[![Build Status](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_apis/build/status/tomtom-international.ebr-board?branchName=master)](https://dev.azure.com/tomtomweb/GitHub-TomTom-International/_build/latest?definitionId=39&branchName=master)


[![PyPI - Version](https://img.shields.io/pypi/v/ebr-board.svg)](https://pypi.org/project/ebr-board/)
[![PyPI - License](https://img.shields.io/pypi/l/ebr-board.svg)](https://pypi.org/project/ebr-board/)
[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/ebr-board.svg)](https://pypi.org/project/ebr-board/)
[![PyPI - Format](https://img.shields.io/pypi/format/ebr-board.svg)](https://pypi.org/project/ebr-board/)
[![PyPI - Status](https://img.shields.io/pypi/status/ebr-board.svg)](https://pypi.org/project/ebr-board/)
[![PyUp - Updates](https://pyup.io/repos/github/tomtom-international/ebr-board/shield.svg)](https://pyup.io/repos/github/tomtom-international/ebr-board/)


RESTful interface for Elastic Build Results.

## Usage

To view the API documentation, start the server and go to to `<url>/api/docs`.

## Configuration

ebr-board uses [Vault-Anyconfig](https://pypi.org/project/vault-anyconfig/) to read in its configuration, allowing it to access a Hashicorp Vault
instance for loading secrets. For more details refer to its documentation.

In order to deploy a simple ebr-board instance, you will need two files: `config.yaml` and `vault.yaml`. Leave `vault.yaml` empty, as we will not use
secret loading from Vault-Anyconfig in this instance.

`config.yaml` should be formatted as follows:

```yaml
elastic:
  host: <elastic_url>
  port: 9200
  timeout: 20
  use_ssl: true
  verify_certs: true
  ca_certs: /etc/ebr-board/elastic.crt
  index: testspipeline*
  user: <elastic_user>
  pwd: <elastic_password>

```


### Dev Mode

To start in dev mode, run ` python ebr_board/ebr_board.py`

### Production Mode

Can be invoked with `ebr_board:create_app(config_filename='/etc/ebr-board/config.yaml', vault_config_filename='/etc/ebr-board/vault.yaml', vault_creds_filename='/etc/ebr-board/vault.yaml', load_certs=True, reverse_proxy=True)`, for example from Gunicorn. You should configure it behind a reverse proxy - for more details see
any guide on configuring Flask servers for deployment. A Dockerfile pre-configuring Gunicorn is available in the root of the repository.

### AWS Lambda Support

The application can be run in AWS Lambda by using the `handler` function in the `aws_lambda` module. In this case it should be installed with the
`aws_lambda` optional dependencies, i.e. `pip install ebr-board['aws_lambda']`.
It expects that the configuration (the main configuration, vault configuration and vault creds) will be stored entirely as strings in the parameter
store. The way it processes these parameters can be configured with environmental variables:
* `config_name`: defaults to `ebr_board_config`
* `vault_config_name`: defaults to `ebr_board_vault_config`
* `vault_creds_name`: defaults to `ebr_board_vault_creds`
* `config_format`: defaults to `yaml`

## Features

* Provides abstraction to fetch:
    * a list of builds from a given job
    * tests from a given job
    * aggregations of tests failures
* AWS Lambda support

### Todo:

* Improve test coverage
* Fill in coverage of resources
* Expand aggregation/search functionality

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [tomtom-international/cookiecutter-python](https://github.com/tomtom-international/cookiecutter-python) project template.
