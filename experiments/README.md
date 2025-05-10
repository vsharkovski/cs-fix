# Experiments

## Reproducing the Results

### 1. Environment Setup

Follow instructions in the [root README](../README.md) for setup, including Pipenv and `.env` file setup.

### 2. Test Directory Setup

**Our own test files:**  
In addition to external repositories, we use three test folders:

- `tests/buggy_test_project`, which we created ourselves
- `tests/buggy-python`, ???
- `tests/Python-new`, ???

These folders are included in this repository under the `tests/` directory and were used to produce the results in the paper.

### 3. Running the Experiments

Ensure your `tests/` folder contains only the three folders mentioned above (and any cloned repositories if used).

While in the virtual environment, with your current working directory being `experiments`, you can run the following commands:

- Scan a repository or folder:

```sh
python -m csfix scan ruff mypy tests/
```

- Show detected problems:

```sh
python -m csfix show tests/
```

- Get suggestions for a file:

```sh
python -m csfix suggest tests/buggy_test_project/example.py
```

- Apply fixes automatically:

```sh
python -m csfix fix tests/buggy_test_project/example.py
```

For help on available commands:

```sh
python -m csfix -h
```

### 4. Using Test Scripts

You can also run `test_metrics.py` to automate and replicate the evaluation process. For example:

```sh
python test_metrics.py
```
