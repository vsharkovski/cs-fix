EXCLUDE_PATTERN="experiments/tests"
EXCLUDE_OPTION="--exclude=$EXCLUDE_PATTERN"

if [ "${IS_GITHUB:-0}" -eq 1 ]; then
    echo "Running ruff linter ..." && \
    pipenv run ruff check $EXCLUDE_OPTION --output-format=github .
else
    echo "Running ruff linter with automatic fixes ..." && \
    pipenv run ruff check $EXCLUDE_OPTION --fix . \

    echo "Running ruff formatter ..." && \
    pipenv run ruff format $EXCLUDE_OPTION .
fi || exit 1

# echo "Running mypy ..." && \
# pipenv run mypy .
