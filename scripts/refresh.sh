#!/usr/bin/env bash
#
# Refresh the training data in Databricks and rebuild the model end to end.
#
#   1. mirror data/pos and data/neg into the bronze Volume (true mirror:
#      remote folders are deleted first, so local deletions propagate)
#   2. deploy the bundle (code + job definition)
#   3. run the job (ingest -> clean -> prepare -> train -> export)
#   4. download the exported model.json to ./models/model.json
#
# Usage:
#   ./scripts/refresh.sh            # default target: dev
#   ./scripts/refresh.sh dev
#
set -euo pipefail

TARGET="${1:-dev}"
DATA_VOLUME="dbfs:/Volumes/workspace/bronze/raw"
ARTIFACT_VOLUME="dbfs:/Volumes/workspace/gold/artifacts"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# Use your own corpus if present, otherwise the small synthetic sample that
# ships with the repo so a fresh clone still runs end to end.
DATA_DIR="data"
if [ ! -d "${DATA_DIR}/pos" ] || [ ! -d "${DATA_DIR}/neg" ]; then
  DATA_DIR="data/sample"
  echo "==> data/pos or data/neg not found; using sample data in ${DATA_DIR}"
fi

echo "==> Uploading training data from ${DATA_DIR} to ${DATA_VOLUME}"
for split in pos neg; do
  # Remove first so files deleted locally also disappear remotely.
  databricks fs rm -r "${DATA_VOLUME}/${split}" 2>/dev/null || true
  databricks fs cp -r "${DATA_DIR}/${split}" "${DATA_VOLUME}/${split}"
done

echo "==> Deploying bundle (target: ${TARGET})"
databricks bundle deploy -t "${TARGET}"

echo "==> Running the pipeline"
databricks bundle run webpage_classifier -t "${TARGET}"

echo "==> Downloading model.json"
mkdir -p models
databricks fs cp --overwrite "${ARTIFACT_VOLUME}/model.json" ./models/model.json

echo "==> Done: models/model.json is up to date"
