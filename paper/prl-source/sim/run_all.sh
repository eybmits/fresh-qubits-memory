#!/bin/bash
# Repository entry point; writes only to a new --output-dir, never supplied data.
# Example (from the repository root):
#   bash paper/prl-source/sim/run_all.sh --output-dir results/local/prl-campaign
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd)"
runner="$repo_root/scripts/run_prl_campaign.py"
if [[ ! -f "$runner" ]]; then
  echo "Use scripts/run_prl_campaign.py from the fresh-qubits-memory repository." >&2
  exit 1
fi
exec python3 "$runner" "$@"
