#!/bin/bash

set -eEuo pipefail
export SHELLOPTS

echo "conda env create begin at $(date --utc +%Y-%m-%dT%H:%M:%S)"

ARGS=("${@}")

CONDA_ENV_YML_PATH="conda_env.yml"

while [[ $# -gt 0 ]]; do
	case $1 in

		--conda-env-yml) CONDA_ENV_YML_PATH=$2; shift; shift;;
		--conda-update-base-f) CONDA_UPDATE_BASE_F=; shift;;
		--conda-use-mamba-solver-f) CONDA_USE_MAMBA_SOLVER_F=; shift;;

		*) shift;;
	esac
done

echo ARGS="${ARGS[@]}"
echo CONDA_ENV_YML_PATH="${CONDA_ENV_YML_PATH}"
echo CONDA_UPDATE_BASE_F=${CONDA_UPDATE_BASE_F+Y}
echo CONDA_USE_MAMBA_SOLVER_F=${CONDA_USE_MAMBA_SOLVER_F+Y}

if [ -v CONDA_UPDATE_BASE_F ]
then

	conda update \
	--name base \
	conda

fi

if [ -v CONDA_USE_MAMBA_SOLVER_F ]
then

	conda install \
	--name base \
	conda-libmamba-solver

	conda config \
	--set solver libmamba

fi

conda env create \
--file "${CONDA_ENV_YML_PATH}" \
--force

conda clean --all --yes

echo "conda env create end at $(date --utc +%Y-%m-%dT%H:%M:%S)"
