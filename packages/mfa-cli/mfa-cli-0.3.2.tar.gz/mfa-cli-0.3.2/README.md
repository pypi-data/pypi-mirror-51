# mfa-cli

[![Build Status](https://travis-ci.org/thiagoalmeidasa/mfa-cli.svg?branch=master)](https://travis-ci.org/thiagoalmeidasa/mfa-cli)

CLI tool for generating one-time passwords.

## Usage

```bash
$ python -m mfa_cli list-keys --keyfile codes.yml
$ python -m mfa_cli new-totp --keyfile codes.yml
$ python -m mfa_cli new-totp --keyfile codes.yml --keyname myservice
```

## Instalation

```bash
pip install mfa-cli
```
