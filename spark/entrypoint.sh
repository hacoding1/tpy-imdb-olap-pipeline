#!/usr/bin/env bash

set -euo pipefail

ROLE="${1:-}"

if [ $# -gt 0 ]; then
    shift
fi

SPARK_MASTER_HOST="${SPARK_MASTER_HOST:-spark-master}"
SPARK_MASTER_PORT="${SPARK_MASTER_PORT:-7077}"
SPARK_MASTER_WEBUI_PORT="${SPARK_MASTER_WEBUI_PORT:-8080}"

SPARK_WORKER_MEMORY="${SPARK_WORKER_MEMORY:-2G}"
SPARK_WORKER_CORES="${SPARK_WORKER_CORES:-2}"

SPARK_MASTER_URL="spark://${SPARK_MASTER_HOST}:${SPARK_MASTER_PORT}"

echo "========================================="
echo "Starting Spark Container"
echo "Role              : ${ROLE}"
echo "Master URL        : ${SPARK_MASTER_URL}"
echo "========================================="

case "${ROLE}" in

    master)
        echo "Starting Spark Master..."

        exec /opt/spark/bin/spark-class \
            org.apache.spark.deploy.master.Master \
            --host "${SPARK_MASTER_HOST}" \
            --port "${SPARK_MASTER_PORT}" \
            --webui-port "${SPARK_MASTER_WEBUI_PORT}"
        ;;

    worker)
        echo "Starting Spark Worker..."

        exec /opt/spark/bin/spark-class \
            org.apache.spark.deploy.worker.Worker \
            --cores "${SPARK_WORKER_CORES}" \
            --memory "${SPARK_WORKER_MEMORY}" \
            "${SPARK_MASTER_URL}"
        ;;

    bash)
        exec /bin/bash
        ;;

    *)
        exec "$@"
        ;;

esac