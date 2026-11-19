#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../../../.." && pwd)"
source "$REPO/scripts/eval-fixtures/maya-profile.sh"
python3 -I "$REPO/scripts/eval-fixtures/maya-resume.py"
