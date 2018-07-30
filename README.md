# GWDataFind

The client library for the LIGO Data Replicator (LDR) service.

The DataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors.

[![pipeline status](https://git.ligo.org/duncanmmacleod/gwdatafind/badges/master/pipeline.svg)](https://git.ligo.org/duncanmmacleod/gwdatafind/commits/master)
[![coverage report](https://git.ligo.org/duncanmmacleod/gwdatafind/badges/master/coverage.svg)](https://git.ligo.org/duncanmmacleod/gwdatafind/commits/master)

<!---
## Installation

The simplest installation is via `pip`:

```bash
python -m pip install gwdatafind
```

This package is also available as a Conda package:

```bash
conda install -c conda-forge gwdatafind
```
-->

## Basic Usage

To find the URLs of all `H1_R` files for the LIGO-Hanford observatory in
a given GPS interval:

```python
>>> from gwdatafind import connect
>>> conn = connect()
>>> conn.find_urls('H', 'H1_R', 1198800018, 1198800618)
```

This can be shortened for single interactions to

```python
>>> from gwdatafind import find_urls
>>> find_urls('H', 'H1_R', 1198800018, 1198800618)
```

## On the command-line

GWDataFind can also be executed via the command-line client, for full details
run

```bash
$ python -m gwdatafind --help
```

<!---
For other documentation, see https://gwdatafind.readthedocs.io.
-->
