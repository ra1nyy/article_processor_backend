#!/bin/bash
case "$1" in
  "backend")
    uvicorn main:app --host 0.0.0.0 --port "$UVICORN_SERVER_PORT" --root-path "$API_PREFIX" --workers "$WORKERS_COUNT"
    ;;
  "pytest")
    pytest -v
    ;;
  "migration")
    alembic upgrade head
    ;;
  *)
    echo "Incorrect parameter to sh script!."
    exit 1
    ;;
esac
