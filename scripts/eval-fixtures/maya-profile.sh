#!/usr/bin/env bash
# Shared eval fixture: loads the fictional Maya Okafor example profile into the
# eval workspace (the current directory). Called from each case's fixture.sh.
# Usage (from a case's fixture.sh): source "$REPO/scripts/eval-fixtures/maya-profile.sh"
set -euo pipefail
: "${REPO:?REPO must be set to the post-to-hired repo root}"
mkdir -p profile
for f in "$REPO"/plugins/setup/skills/setup/example/maya-okafor/*.md; do
  [ "$(basename "$f")" = "README.md" ] && continue
  cp "$f" profile/
done
git init -q . 2>/dev/null || true
printf 'profile/\ntracker/\n' > .gitignore
