#!/usr/bin/env bash
# Gate that must pass before anything is pushed to GitHub.
# Runs automatically from .githooks/pre-push once `git config core.hooksPath .githooks` is set.
# Run by hand from the repo root: scripts/pre-push.sh
#
# 1. Plugin validation   (claude plugin validate)
# 2. File references     (every file a skill points to ships inside its plugin)
# 3. Privacy scan        (generic checks + your local private-terms list)
# 4. Evals               (claude plugin eval on all three plugins, every case; shell access
#                         is granted only inside the eval sandbox)
#
# Options (environment variables):
#   EVAL_THRESHOLD   minimum score per case, 0..1        (default 0.8)
#   EVAL_MAX_COST    cost ceiling in USD for all evals    (default 15)
#   EVAL_RUNS        runs per case                       (default: each case's runs, 3)
#   EVAL_CONCURRENCY parallel eval runs                  (default 3)
#   PRIVATE_TERMS    path to your private terms list     (default .private-terms)
set -uo pipefail
cd "$(git rev-parse --show-toplevel)"

fail=0
step() { printf '\n== %s\n' "$1"; }
bad()  { printf '   FAIL: %s\n' "$1"; fail=1; }
ok()   { printf '   ok: %s\n' "$1"; }

PLUGINS=(setup linkedin-content job-search)

# Everything below checks the files git tracks or is about to commit, not stray local files.
tracked() { git ls-files -co --exclude-standard; }

step "1/4 Plugin validation"
if claude plugin validate . >/tmp/ptoh-validate.log 2>&1; then ok "marketplace"; else bad "marketplace"; cat /tmp/ptoh-validate.log; fi
for p in "${PLUGINS[@]}"; do
  if claude plugin validate "plugins/$p" >/tmp/ptoh-validate.log 2>&1; then ok "$p"; else bad "$p"; cat /tmp/ptoh-validate.log; fi
done

step "2/4 File references inside each plugin"
tmp=$(mktemp -d)
for p in "${PLUGINS[@]}"; do cp -r "plugins/$p" "$tmp/"; done
if python3 -I scripts/check-refs.py "$tmp"; then ok "all references resolve"; else bad "missing references"; fi
rm -rf "$tmp"

step "3/4 Privacy scan"
files=$(tracked | grep -v '^scripts/pre-push.sh$')
# Email addresses other than reserved example domains and no-reply addresses
emails=$(echo "$files" | xargs grep -noiE '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}' 2>/dev/null \
         | grep -viE '@example\.(com|org)|noreply@|users\.noreply\.github\.com' || true)
[ -z "$emails" ] && ok "no personal email addresses" || { bad "email addresses found"; echo "$emails"; }
paths=$(echo "$files" | xargs grep -nE '/Users/[A-Za-z]|/home/[a-z]+/|Library/Application Support|C:\\Users' 2>/dev/null || true)
[ -z "$paths" ] && ok "no paths from someone's computer" || { bad "machine paths found"; echo "$paths"; }
binaries=$(echo "$files" | grep -iE '\.(docx|pdf|csv|xlsx|skill|zip|png|jpe?g)$' || true)
[ -z "$binaries" ] && ok "no resume, document or image files" || { bad "files that should not be published"; echo "$binaries"; }
notes=$(echo "$files" | grep -iE 'call-notes|(^|/)profile/|(^|/)tracker/' | grep -v '/evals/' || true)
[ -z "$notes" ] && ok "no profile, tracker or call-notes files" || { bad "private files tracked"; echo "$notes"; }
TERMS_FILE="${PRIVATE_TERMS:-.private-terms}"
if [ -f "$TERMS_FILE" ]; then
  hits=$(echo "$files" | xargs grep -niwFf <(grep -vE '^\s*(#|$)' "$TERMS_FILE") 2>/dev/null || true)
  [ -z "$hits" ] && ok "none of your private terms ($TERMS_FILE)" || { bad "private terms found"; echo "$hits"; }
  # Also check the commits about to be pushed, including deleted lines
  upstream=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || echo "")
  range=${upstream:+$upstream..HEAD}
  hist=$(git log -p ${range:-HEAD} 2>/dev/null | grep -iwFf <(grep -vE '^\s*(#|$)' "$TERMS_FILE") || true)
  [ -z "$hist" ] && ok "commits being pushed are clean" || { bad "private terms in commits being pushed"; echo "$hist" | head -20; }
else
  printf '   WARN: no %s file, so your own names and details were not checked.\n         Create it (one term per line, it is gitignored) to enable this check.\n' "$TERMS_FILE"
fi

if [ "$fail" -ne 0 ]; then
  printf '\nStatic checks failed. Fix them before running evals.\n'; exit 1
fi

step "4/4 Evals (all cases, all plugins)"
# The eval runner only grants shell access inside a sandbox. On Linux that needs bubblewrap and socat
# (macOS has its sandbox built in). Without them every case with shell access is refused, not run.
if [ "$(uname -s)" = "Linux" ] && ! { command -v bwrap >/dev/null && command -v socat >/dev/null; }; then
  bad "eval sandbox missing: install bubblewrap and socat (e.g. sudo apt-get install -y bubblewrap socat)"
  exit 1
fi
EVAL_THRESHOLD="${EVAL_THRESHOLD:-0.8}"
EVAL_MAX_COST="${EVAL_MAX_COST:-15}"
runs_flag=(); [ -n "${EVAL_RUNS:-}" ] && runs_flag=(--runs "$EVAL_RUNS")
outdir="$(mktemp -d)"
for p in "${PLUGINS[@]}"; do
  printf '   running %s evals...\n' "$p"
  claude plugin eval "plugins/$p" \
    --trust-plugin --scaffold --ablation none --no-publish \
    --threshold "$EVAL_THRESHOLD" --max-cost-usd "$EVAL_MAX_COST" "${runs_flag[@]}" \
    --concurrency "${EVAL_CONCURRENCY:-3}" \
    --allow-tools Write Edit WebFetch WebSearch Agent Bash \
    --json "$outdir/$p.json" >"$outdir/$p.log" 2>&1
  code=$?
  summary=$(python3 -I - "$outdir/$p.json" "$EVAL_THRESHOLD" <<'PY' 2>/dev/null
import json, sys
d = json.load(open(sys.argv[1]))
a = d.get("aggregates", {})
print(f"{a.get('casesPassed','?')}/{a.get('casesTotal','?')} cases passed, score {a.get('overallScore','?')}, cost ${d.get('costUsd',0):.2f}"
      + (f", PARTIAL: {d.get('partialReason')}" if d.get("partial") else ""))
for c in d.get("cases", []):
    s = c.get("aggregates", {}).get("score")
    print(f"      {'ok  ' if s is not None and s >= float(sys.argv[2] if len(sys.argv) > 2 else 0.8) else 'FAIL'} {c.get('name')}: {s}")
PY
)
  echo "$summary" | sed 's/^/   /'
  if [ "$code" -ne 0 ]; then bad "$p evals (exit $code, log: $outdir/$p.log)"; else ok "$p evals"; fi
done

if [ "$fail" -ne 0 ]; then
  printf '\nPush blocked: fix the failures above. Eval details are in %s\n' "$outdir"; exit 1
fi
printf '\nAll checks passed. Safe to push.\n'
