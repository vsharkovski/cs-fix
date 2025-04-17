import os
from pathlib import Path


def get_env_var_or_throw(key: str) -> str:
    value = os.environ.get(key)

    # Check that value is not None and not empty.
    if not value:
        raise EnvironmentError(f"Missing required {key}")

    return value


def glob_files_resolved(directory: Path, pattern: str) -> list[Path]:
    return [path.resolve() for path in directory.glob(pattern) if path.is_file()]
