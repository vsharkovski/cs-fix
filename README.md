# CS-Fix

This directory contains the components of CS-Fix.

* [`csfix`](./csfix/): CS-Fix backend, a command-line tool.
* [`scripts`](./scripts/): Scripts for development and running.
* [`experiments`](./experiments/): Scripts for experiments and evaluation.

## Pre-requisites

* Python 3.10 or higher
* [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Running Locally

### Setting up the environment

1. Install [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

2. Install dependencies (including development dependencies): `pipenv sync --dev`

3. Create an `.env` file in this directory and configure it (see [`.sampleenv`](./.sampleenv))

### Running

While in the project root directory, run [`scripts/run.sh`](./scripts/run.sh).

### Linting

To lint the code with Ruff and Mypy, while in the project root directory, run [`scripts/lint.sh`](./scripts/lint.sh).

### Cleaning up

To clean up generated files, while in the project root directory, run [`scripts/clean.sh`](./scripts/clean.sh).
