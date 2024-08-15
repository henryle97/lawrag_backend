find lawrag -name "*.py" -not -path "lawrag/apps/engine/migrations/*" \
    -not -path "lawrag/apps/cron/migrations/*" | xargs python -m isort


find lawrag -name "*.py" -not -path "lawrag/apps/engine/migrations/*" \
    -not -path "lawrag/apps/cron/migrations/*" | xargs python -m black -l 79

