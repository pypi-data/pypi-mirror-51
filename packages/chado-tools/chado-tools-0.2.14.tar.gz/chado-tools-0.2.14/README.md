# chado-tools

Python3 command line script providing various tools for accessing CHADO databases.

[![Build Status](https://travis-ci.org/sanger-pathogens/chado-tools.svg?branch=master)](https://travis-ci.org/sanger-pathogens/chado-tools)   
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/sanger-pathogens/chado-tools/blob/master/LICENSE)   
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat-square)](http://bioconda.github.io/recipes/chado-tools/README.html)   
[![Container ready](https://img.shields.io/badge/container-ready-brightgreen.svg)](https://quay.io/repository/biocontainers/chado-tools)   
[![Docker Build Status](https://img.shields.io/docker/cloud/build/sangerpathogens/chado-tools.svg)](https://hub.docker.com/r/sangerpathogens/chado-tools)   
[![Docker Pulls](https://img.shields.io/docker/pulls/sangerpathogens/chado-tools.svg)](https://hub.docker.com/r/sangerpathogens/chado-tools)   
[![codecov](https://codecov.io/gh/sanger-pathogens/chado-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/sanger-pathogens/chado-tools)

## Contents
  * [Installation](#installation)
    * [Required dependencies](#required-dependencies)
    * [From source](#from-source)
    * [Using pip](#using-pip)
    * [Using Bioconda](#using-bioconda)
    * [Using a Docker container](#using-a-docker-container)
  * [Usage](#usage)
    * [Database connection](#database-connection)
    * [Available commands](#available-commands)
    * [Examples](#examples)
    * [Note concerning tests](#note-concerning-tests)
  * [License](#license)
  * [Feedback/Issues](#feedback/issues)

## Installation
There are a number of ways to install chado-tools and details are provided below. If you encounter an issue when installing chado-tools please contact your local system administrator. If you encounter a bug please log it [here](https://github.com/sanger-pathogens/chado-tools/issues) or email us at path-help@sanger.ac.uk.

### Required dependencies
* Python 3.6
* PostgreSQL 9.6 or higher

### From source
Download the latest release from this github repository, or clone the repository to obtain the most recent updates.
Then install the software:

    python3 setup.py install

For running tests please see the [note](#note-concerning-tests) below.

### Using pip
You can install the program from the [Python Package Index (PyPI)](https://pypi.org/project/chado-tools/) using the command

    pip install chado-tools

### Using Bioconda
The program is also available as [Bioconda package](https://anaconda.org/bioconda/chado-tools). Install it with the command

    conda install -c bioconda chado-tools

### Using a Docker container
The program is also available as a standalone Docker container. The latest build can be downloaded from [DockerHub](https://hub.docker.com/r/sangerpathogens/chado-tools) with the command

    docker pull sangerpathogens/chado-tools

When running the container with Docker, use the flags `--interactive --tty` and map all required environment variables (see below) with flag `--env`.


## Usage
The installation will put a single script called `chado` in your PATH.
The usage is:

    chado <command> [<subcommand>] [options]

* To list the available commands and brief descriptions, just run `chado -h` or `chado --help`.
* To display the version of the program, type `chado -v` or `chado --version`.
* Use `chado <command> -h` or `chado <command> --help` to get a detailed description and the usage of that command.

### Database connection
You can set up default values for database host, port and user with environment variables. To do so, add the following 
lines to your `.bashrc` (replacing the example values):

    export CHADO_HOST=localhost
    export CHADO_PORT=5432
    export CHADO_USER=chadouser

The software seeks for these environment variables on your system. If they do not exist, it will use the 
[default connection settings](pychado/data/defaultDatabase.yml), which you can edit manually if you really want.

Analogously, you can specify a default password with the environment variable `CHADO_PASS`.
The flag `-p` enforces asking the user for a password, which is useful if you don't want to store a default password in your environment.

Alternatively, you can supply your own YAML configuration file in the same format as the [default file](pychado/data/defaultDatabase.yml)
with flag `-c` (including password). The software will then ignore any environment variables. 


### Available commands

------------------------------------------------------------------------------------------------
| Command               | Description                                                          |
|-----------------------|----------------------------------------------------------------------|
| connect               | connect to a CHADO database for an interactive session               |
| query                 | query a CHADO database and export the result into a text file        |
| execute               | execute a function defined in a CHADO database                       |
| extract               | run a pre-compiled query against the CHADO database                  |
| insert                | insert a new entity of a specified type into the CHADO database      |
| delete                | delete an entity of a specified type from the CHADO database         |
| import                | import data from file into the CHADO database                        |
| export                | export data from the CHADO database to file                          |
| admin                 | perform admin tasks, such as creating or dumping a CHADO database    |
------------------------------------------------------------------------------------------------

### Examples
Create a new CHADO database called `eukaryotes` according to the current GMOD schema:

    chado admin create eukaryotes
    chado admin setup -s gmod eukaryotes
    
Dump this database into an archive called `eukaryotes.dump`:

    chado admin dump eukaryotes eukaryotes.dump

List all organisms in the `eukaryotes` database:

    chado extract organisms eukaryotes

Query the database to check the meaning of a certain `cvterm_id`:

    chado query -q "SELECT name FROM cvterm WHERE cvterm_id = 25" eukaryotes

Export a FASTA file containing the sequences of the organism `Pfalciparum`:

    chado export fasta -a Pfalciparum -o Pfalciparum.fasta -t contigs eukaryotes

### Note concerning tests
Some of the integration tests rely on access to a PostgreSQL server. In order to successfully run those tests, 
modify the [default connection settings](pychado/data/defaultDatabase.yml) such that they describe an existing 
PostgreSQL database server to which you can connect. The tests can then be run as `python3 setup.py test`.
They create temporary databases on that server and clean those up when finished, so this shouldn't interfere with
anything you have stored in any database on that server. If you are concerned about this, though, make sure to point
the tool to an empty test server.

## License
chado-tools is free software, licensed under [GPLv3](https://github.com/sanger-pathogens/chado-tools/blob/master/LICENSE).

## Feedback/Issues
Please report any issues to the [issues page](https://github.com/sanger-pathogens/chado-tools/issues) or email path-help@sanger.ac.uk.
