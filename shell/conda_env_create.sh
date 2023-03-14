#!/bin/bash

set -eEuo pipefail
export SHELLOPTS

echo "conda env create begin at $(date --utc +%Y-%m-%dT%H:%M:%S)"

ARGS=("${@}")

CONDA_ENV_YML_PATH="conda_env.yml"

while [[ $# -gt 0 ]]; do
	case $1 in

		--conda-env-yml) CONDA_ENV_YML_PATH=$2; shift; shift;;

		*) shift;;
	esac
done

echo ARGS="${ARGS[@]}"
echo CONDA_ENV_YML_PATH="${CONDA_ENV_YML_PATH}"

conda update \
--name base \
conda

conda-env create \
--file "${CONDA_ENV_YML_PATH}" \
--force

conda clean --all --yes

echo "conda env create end at $(date --utc +%Y-%m-%dT%H:%M:%S)"
