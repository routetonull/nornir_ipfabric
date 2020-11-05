![Stars](https://img.shields.io/github/stars/routetonull/nornir_ipfabric?style=social)

![LastCommit](https://img.shields.io/github/last-commit/routetonull/nornir_ipfabric)

[![Version](https://img.shields.io/pypi/v/nornir-ipfabric)](https://pypi.org/project/nornir-ipfabric/)







nornir_ipfabric
==============

[IPFabric](https://ipfabric.io/) Inventory plugin for [nornir](https://github.com/nornir-automation/nornir).


# Install

The recommended way to install nornir_ipfabric is via pip

```sh
pip install nornir-ipfabric
```


# Requirements

An instance of [IP Fabric](https://ipfabric.io/) is required to collect information. [Request trial license.](https://ipfabric.io/booking-trial/)


# Example usage

## Using env vars

Set environment vars to provide url and credentials to connect to the IP Fabric server

```sh
export IPF_URL=https://ipfabric.local
export IPF_USER=admin
export IPF_PASSWORD=mySecretPassword
```

## Using the InitNornir function

```python
from nornir import InitNornir
nr = InitNornir(
    inventory=
        {
            "plugin": "IPFabricInventory", 
            "options": {
                "ipf_url":"https://ipfabric.local",
                "ipf_user":"admin",
                "ipf_password":"mySecretPassword",
                },
        },
    )
```

## Using the Nornir configuration file

File *config.yaml*

```yaml
---
inventory:
  plugin: IPFInventory
  options:
    ipf_url: "https://ipfabric.local"
    ipf_user: "admin"
    ipf_password: "mySecretPassword"
```

Usage:

```python
from nornir import InitNornir
nr = InitNornir(config_file="config.yaml",inventory={"plugin": "IPFabricInventory"})
```



# Useful Links

- [IP Fabric website](https://www.ipfabric.io)
- [IP Fabric channel on Slack ](https://networktocode.slack.com/)
- [Nornir](https://github.com/nornir-automation/nornir)
- [Nornir Discourse Group](https://nornir.discourse.group)
- [An Introduction to Nornir](https://pynet.twb-tech.com/blog/nornir/intro.html)