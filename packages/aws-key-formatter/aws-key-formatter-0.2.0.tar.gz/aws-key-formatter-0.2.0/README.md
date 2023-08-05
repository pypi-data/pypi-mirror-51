# aws-key-formatter

Project/Repo:

[![MIT License][license_img]][license_ref]
[![Supported Python Versions][pyversions_img]][pyversions_ref]
[![aws-key-formatter v0.0.4][version_img]][version_ref]
[![PyPI Releases][pypi_img]][pypi_ref]
[![PyPI Downloads][downloads_img]][downloads_ref]

Code Quality/CI:

[![Build Status][travis_img]][travis_ref]

## Overview

This CLI will take your AWS credentials and output them in various formats.

The initial use case is for displaying your AWS credentials for use as the
`Authorization` parameter in several AWS Redshift commands.

See [Use Cases](#use-cases) for all possible output formats.

## Installation

`aws-key-formatter` can be installed by running:

```bash
pip install aws-key-formatter
```

It requires Python 3.6+ to run.

You can, also, install via [`pipx`](https://pipxproject.github.io/pipx/):

```bash
pipx install aws-key-formatter
```

## Usage

### Redshift

To use your AWS credentials as the `Authorization` parameter in a Redshift
command (See [the Redshift docs](https://docs.aws.amazon.com/redshift/latest/dg/copy-parameters-authorization.html#copy-access-key-id)):

```bash
$ aws-key-formatter redshift
ACCESS_KEY_ID '<access-key-id>'
SECRET_ACCESS_KEY '<secret-access-key>'

# If you want the session token included as well
$ aws-key-formatter redshift --token
ACCESS_KEY_ID '<access-key-id>'
SECRET_ACCESS_KEY '<secret-access-key>'
SESSION_TOKEN '<temporary-token>'
```

### Environment Variables

To use your AWS credentials as [environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html):

```bash
$ aws-key-formatter env
AWS_ACCESS_KEY_ID=<access-key-id>
AWS_SECRET_ACCESS_KEY=<secret-access-key>

# If you want the session token included as well
$ aws-key-formatter env --token
ACCESS_KEY_ID=<access-key-id>
SECRET_ACCESS_KEY=<secret-access-key>
SESSION_TOKEN=<temporary-token>
```

## Contributing

<!-- TODO: add some contributing guidelines -->

<!-- References -->

[downloads_img]: https://pepy.tech/badge/aws-key-formatter/month
[downloads_ref]: https://pepy.tech/project/aws-key-formatter

[license_img]: https://img.shields.io/badge/License-MIT-blue.svg
[license_ref]: https://github.com/KeltonKarboviak/aws-key-formatter/blob/master/LICENSE.md

[pypi_img]: https://img.shields.io/badge/PyPI-wheels-green.svg
[pypi_ref]: https://pypi.org/project/aws-key-formatter/#files

[pyversions_img]: https://img.shields.io/pypi/pyversions/aws-key-formatter.svg
[pyversions_ref]: https://pypi.org/pypi/aws-key-formatter

[travis_img]: https://travis-ci.org/KeltonKarboviak/aws-key-formatter.svg?branch=master
[travis_ref]: https://travis-ci.org/KeltonKarboviak/aws-key-formatter

[version_img]: https://img.shields.io/static/v1.svg?label=aws-key-formatter&message=v0.2.0&color=blue
[version_ref]: https://pypi.org/project/aws-key-formatter/
