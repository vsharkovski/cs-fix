# CS-Fix

This directory contains the components of CS-Fix.

* [`csfix`](./csfix/): CS-Fix backend, a command-line tool.
* [`scripts`](./scripts/): Scripts for development and running.
* [`experiments`](./experiments/): Scripts for experiments and evaluation.

## Pre-requisites

* Python 3.10. Other Python versions are not supported currently.
* [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Running Locally

### Setting up the environment

1. Install [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

2. Install dependencies (including development dependencies): `pipenv sync --dev`

3. Create an `.env` file in the project root directory and configure it (see [`.sampleenv`](./.sampleenv))

### Activating the virtual environment

Every time you want to run or develop the project, you have to activate the virtual environment created by pipenv:

```sh
pipenv shell
```

### Running

While in the virtual environment, do:
```sh
python -m csfix <arguments>
```

For example, to get help:
```sh
python -m csfix -h
python -m csfix scan -h
python -m csfix show -h
python -m csfix suggest -h
```

### Cleaning up

To clean up generated files, while in the project root directory, run [`./scripts/clean.sh`](./scripts/clean.sh).

## Reproducing experiments

See [`experiments/README.md`](./experiments/README.md).

## Development

### Dependencies

For installing/managing dependencies, use `pipenv` instead of `pip`. Pipenv automatically manages dependencies and virtual environments, so you don't have to create a virtual environment either.

If you get errors from Pylance, make sure you are using the correct Python interpreter:
1. Open command palette (`ctrl + shift + P`)
2. Type `Python: Select Interpreter`
3. Select the interpreter created by Pipenv. It should look something like `Python 3.10.12 ('cs-fix'VL8dbg2y': Pipenv)`.

### Linting

There are linters which check and format your code automatically. To run them, while in the virtual environment, run the script [`./scripts/lint.sh`](./scripts/lint.sh).
