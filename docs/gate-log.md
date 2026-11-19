# Gate failure log

Every time `scripts/pre-push.sh` blocks a push, record it here: what failed, the real cause, the fix, and
the guard added so the same problem can't pass silently again. Newest first.

Causes fall into three kinds:
- **Skill**: the skill did the wrong thing. Fix the skill.
- **Grader**: the skill was right, the check was wrong. Fix the grader in `scripts/gen-evals.py`.
- **Setup**: the test environment or the gate itself was wrong. Fix the gate or the fixtures.

---

## 2026-11-19 · `humanizer-strawman-contrast` (0.7999999999999999) blocked the next push
- **Kind:** Setup (the gate) and Skill.
- **Setup cause:** The case averaged (0.4 + 1 + 1) / 3, exactly 0.8, but floating-point rounding made it 0.7999999999999999, below the 0.8 threshold. A case right at the threshold failed.
- **Skill cause:** In 1 of 3 runs the humanizer wrote a sample fact into the rewrite ("told me a company had raised a Series B") and added a guessed claim ("Tweaking the prompt didn't hold"), flagged only in a note. That breaks its own first rule: never add ideas that weren't in the original.
- **Fixes:** The gate compares scores against the threshold minus one billionth, for the pass/fail call, the summary and the history. The humanizer has a new rule 9: placeholders are brackets only, with no sample facts and no labeled guesses.
- **Guard:** New grader `no-new-claims` on the humanizer case. It judges only factual statements, so rewording doesn't count.

## 2026-11-19 · `mock-interview-debrief` (0.79) blocked the humanizer push
- **Kind:** Skill (four causes), found by reading traces instead of re-running. This case had failed 3 of its last 5 gate runs.
- **What happened:** Some runs said the resume couldn't be read. Some showed one total per answer instead of per-dimension scores, or dropped the readiness score. One rewrite added unmarked details ("on my own", "I suggested the pilot").
- **Causes:**
  1. The resume-to-text step lived in Phase 1, which a debrief of a pasted transcript skips.
  2. The debrief agent was launched **in the background** (the trace shows "Async agent launched"). The main conversation didn't wait, wrote its own debrief, and the agent's format and checks never reached the user.
  3. The scorecard asked for one column per rubric dimension. With 9 dimensions that's a 12-column table, and the model kept collapsing it to totals.
  4. Inferred details in short follow-up rewrites weren't marked.
- **Fixes:** Resume extraction moved to "Before any agent runs", which always runs, and both agents can extract `.docx`/`.pdf` themselves. Phase 3 now follows the debrief instructions directly instead of launching an agent, and the researcher agent must run in the foreground. The scorecard is now one row per dimension and one column per answer. Every sentence of every rewrite is checked, and inferences are marked `[confirm: ...]`.
- **Guard:** New graders `resume-was-read` (debrief) and `researcher-agent-not-backgrounded` (prep). The story-bank grader accepts `[confirm: ...]` and fails unmarked inventions. The gate records every case's score in `.gate-history.tsv` and prints **REPEAT FAILURE** when a case fails 2 or more of its last 5 runs.
- **Result:** The case went from 0.79 to 0.97 on a 3-run check.
- **Lesson:** When an agent's output format keeps getting lost, check whether the agent's result was actually used before tightening the format.

## 2026-11-19 · Debrief and tailor-resume failures (gated pushes 3 to 6)
- **Kind:** Skill and Grader.
- **Skill causes:** The debrief agents couldn't read `.docx`. The skill condensed the scorecard to one total and dropped the readiness score. Tailor-resume's "new wording" list missed claims, and its headline claimed "Director-level" for a Senior PM.
- **Grader causes:** Hand-typed lists of resume and story-bank facts were incomplete ("6 months", "a quarter of work"), so faithful output was called invented. Prep advice in the brief was read as in-interview coaching. Haiku misjudged a plain "Q1 32, Q2 12" comparison three times.
- **Fixes:** Resume passed to agents as text; a fixed debrief template; line-by-line new-wording check; no title inflation; graders read the real fixture text (resume and story bank) instead of hand-typed lists; Sonnet judges by default.
- **Guard:** Graders that quote facts must read them from `scripts/eval-fixtures/` or the bundled example, never a hand-typed list.

## 2026-11-19 · Many failures on the first full run
- **Kind:** Grader.
- **Cause:** Each LLM grader checked several conditions at once, so one doubt failed the whole case and the report couldn't say which condition broke. One run per case was too noisy for a gate.
- **Fix:** One condition per grader. Three runs per case, scored on the mean.
- **Guard:** `CLAUDE.md` rule: one condition per grader.

## 2026-11-19 · `posts/` flagged as a missing file
- **Kind:** Setup.
- **Cause:** `check-refs.py` didn't know `posts/` is a folder in the user's working directory, like `profile/` and `tracker/`.
- **Fix and guard:** Added `posts/` to the user-side folder list in `scripts/check-refs.py`.

## 2026-11-19 · Every case with shell access refused on the first gate run
- **Kind:** Setup.
- **Cause:** The eval runner only grants shell access inside a sandbox, and this Linux machine lacked `bubblewrap` and `socat`. Cases were refused, not run, and scored near zero.
- **Fix:** Installed both.
- **Guard:** The gate now checks for the sandbox before running evals and stops with install instructions.
