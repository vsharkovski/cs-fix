if [ "${IS_GITHUB:-0}" -eq 1 ]; then
    echo "Running ruff linter ..." && \
    pipenv run python -m ruff check --output-format=github .
else
    echo "Running ruff linter with automatic fixes ..." && \
    pipenv run python -m ruff check --fix .
fi || exit 1

echo "Running ruff formatter ..." && \
pipenv run python -m ruff format . && \

echo "Running mypy ..." && \
pipenv run python -m mypy .
