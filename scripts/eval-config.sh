#!/usr/bin/env bash
# Shared settings for every eval run: the pre-push gate and single-case runs alike.
# Source it:  source scripts/eval-config.sh
#
# Every test runs on Sonnet at medium effort. Override any of these in the environment
# for a one-off experiment, but the gate's defaults are what count for a push.

# Model that runs the skills under test
export EVAL_MODEL="${EVAL_MODEL:-claude-sonnet-5-5}"
# Reasoning effort for those runs. Passed to the eval's Claude runs through
# CLAUDE_CODE_EFFORT_LEVEL, which the runner carries into each run (checked 2026-11-19).
export EVAL_EFFORT="${EVAL_EFFORT:-medium}"
export CLAUDE_CODE_EFFORT_LEVEL="$EVAL_EFFORT"
# Model that grades the outputs
export EVAL_JUDGE_MODEL="${EVAL_JUDGE_MODEL:-claude-sonnet-5-5}"
export EVAL_THRESHOLD="${EVAL_THRESHOLD:-0.8}"
export EVAL_CONCURRENCY="${EVAL_CONCURRENCY:-3}"

# Run one plugin's evals, or one case with a case name:
#   run_eval job-search mock-interview-debrief out.json
run_eval() {
  local plugin="$1" case_name="${2:-}" json="${3:-/dev/null}"
  local case_flag=(); [ -n "$case_name" ] && case_flag=(--case "$case_name")
  local runs_flag=(); [ -n "${EVAL_RUNS:-}" ] && runs_flag=(--runs "$EVAL_RUNS")
  local cmp; cmp=$(python3 -I -c "import sys; print(float(sys.argv[1]) - 1e-9)" "$EVAL_THRESHOLD")
  claude plugin eval "plugins/$plugin" "${case_flag[@]}" \
    --trust-plugin --scaffold --ablation none --no-publish \
    --model "$EVAL_MODEL" --judge-model "$EVAL_JUDGE_MODEL" \
    --threshold "$cmp" --max-cost-usd "${EVAL_MAX_COST:-15}" "${runs_flag[@]}" \
    --concurrency "$EVAL_CONCURRENCY" \
    --allow-tools Write Edit WebFetch WebSearch Agent Bash \
    --json "$json"
}
