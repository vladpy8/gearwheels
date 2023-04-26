#!/bin/bash

set -eEuo pipefail
export SHELLOPTS

echo "pdm publish begin at $(date --utc +%Y-%m-%dT%H:%M:%S)"

pdm publish \
--username "" \
--password ""

echo "pdm publish end at $(date --utc +%Y-%m-%dT%H:%M:%S)"
