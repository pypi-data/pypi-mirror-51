# Tormor Command Line Tool
[![PyPI version](https://badge.fury.io/py/tormor.svg)](https://badge.fury.io/py/tormor)
[![CircleCI](https://circleci.com/gh/Proteus-tech/tormor.svg?style=svg)](https://circleci.com/gh/Proteus-tech/tormor)
[![Coverage Status](https://coveralls.io/repos/github/Proteus-tech/tormor/badge.svg)](https://coveralls.io/github/Proteus-tech/tormor)

Tormor is a command line tool for migrating database. To use Tormor, please first ensure these requirements:

  - Postgresql has been installed
  - Postgresql can be accessed using command :
    ```sh
    $ psql
    ```
- SCHEMA_PATH has been specified
    
## Installation
Tormor requires Python 3.5 or later to run. Tormor can be installed using pip:
```sh
$ pip install git+https://github.com/Proteus-tech/tormor.git@pytest_asyncpg_dryrun
```

## Instruction
    $ tormor [opts] command [args]
For more information, please use command:
```sh
$ tormor --help
```

### Enabling Modules
`enable-modules` command receives module name as a parameter to be enabled and later migrated using `migrate` command.
```
$ tormor enable-modules module-to-be-migrated
```

### Migrate
`migrate` command executes sql files under the enabled modules.
To start migration, use the following command:
```sh
$ tormor migrate
```
To simply output migration sql queries without executing them, use the following command.
```sh
$ tormor migrate --dry-run
```

### Run a Script File
`include` command takes filename as a parameter allows tormor commands to be run in a script, each line at a time.
```sh
$ tormor include filename
```

### Execute SQL File
`sql` command takes filename as a parameter and load and execute the query inside it.
```sh
$ tormor sql filename
```

## Dev

### Requirements
- flit
- PostgreSQL

```bash
pip install flit
flit install
./runtests
```

### Publish to PyPI
```
flit publish
```
