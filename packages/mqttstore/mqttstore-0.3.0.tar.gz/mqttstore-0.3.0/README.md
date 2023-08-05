# `mqttstore` Python Package

[![pipeline status](https://gitlab.com/tue-umphy/co2mofetten/python3-mqttstore/badges/master/pipeline.svg)](https://gitlab.com/tue-umphy/co2mofetten/python3-mqttstore/commits/master)
[![coverage report](https://gitlab.com/tue-umphy/co2mofetten/python3-mqttstore/badges/master/coverage.svg)](https://tue-umphy.gitlab.io/co2mofetten/python3-mqttstore/coverage-report/)
[![documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)](https://tue-umphy.gitlab.io/co2mofetten/python3-mqttstore)
[![PyPI](https://badge.fury.io/py/mqttstore.svg)](https://badge.fury.io/py/mqttstore)

`mqttstore` is a Python package store MQTT data to an SQLite Database.

## Installation

First, make sure you have a recent version of `setuptools`:

```bash
python3 -m pip install --user --upgrade setuptools
```

Then, to install, run from the repository root:

```bash
python3 -m pip install --user .
```

or install it from [PyPi](https://pypi.org/project/mqttstore):

```bash
python3 -m pip install --user mqttstore
```

(Run `sudo apt-get update && sudo apt-get -y install python3-pip` if it
complains about `pip` not being found)

## What can `mqttstore` do?

- store MQTT data to an SQLite database following user-defined rules
- a systemd user service file is also provided

## Documentation

Documentation of the `mqttstore` package can be found [here on
GitLab](https://tue-umphy.gitlab.io/co2mofetten/python3-mqttstore/).

Also, the command-line help page `mqttstore -h` is your friend.
