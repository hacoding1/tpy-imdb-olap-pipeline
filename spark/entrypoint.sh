#!/usr/bin/env bash

set -euo pipefail

ROLE="${1:-}"

# Remove the first argument so remaining args can be passed through
if [ $# -gt 0 ]; then
    shift
fi

SPARK_MASTER_HOST="${SPARK_MASTER_HOST:-spark-master}"
SPARK_MASTER_PORT="${SPARK_MASTER_PORT:-7077}"
SPARK_MASTER_URL="spark://${SPARK_MASTER_HOST}:${SPARK_MASTER_PORT}"

SPARK_WORKER_MEMORY="${SPARK_WORKER_MEMORY:-2G}"
SPARK_WORKER_CORES="${SPARK_WORKER_CORES:-2}"

echo "========================================="
echo "Spark Container Starting"
echo "Role              : ${ROLE}"
echo "Master URL        : ${SPARK_MASTER_URL}"
echo "Worker Memory     : ${SPARK_WORKER_MEMORY}"
echo "Worker Cores      : ${SPARK_WORKER_CORES}"
echo "========================================="

case "${ROLE}" in

    master)
        echo "Starting Spark Master..."

        exec /opt/spark/bin/spark-class \
            org.apache.spark.deploy.master.Master \
            --host "${SPARK_MASTER_HOST}" \
            --port "${SPARK_MASTER_PORT}"
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
        echo "Executing custom command..."
        exec "$@"
        ;;

esac