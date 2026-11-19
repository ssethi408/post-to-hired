# post-to-hired: working rules

## Before any push to GitHub
Every push must pass `scripts/pre-push.sh`. It runs:
1. `claude plugin validate` on the marketplace and all three plugins
2. `scripts/check-refs.py`: every file a skill points to ships inside its own plugin
3. A privacy scan: no personal emails, machine paths, resumes or profile/tracker files, plus the
   terms in the local, gitignored `.private-terms` file
4. `claude plugin eval` on all three plugins (the cases in `plugins/*/evals/`)

The git pre-push hook in `.githooks/` runs it automatically. The SessionStart hook in
`.claude/settings.json` sets `core.hooksPath` for you; if it is not set, run
`git config core.hooksPath .githooks`. Never bypass it with `--no-verify`. If it fails,
fix the cause and run it again; report the failure to the user rather than pushing.

## When you change a skill
- Add or update the eval case for the behavior you changed in `scripts/gen-evals.py`, then run
  `python3 -I scripts/gen-evals.py` to regenerate `plugins/*/evals/`. Don't hand-edit the generated case files.
- One condition per grader, so a failure says exactly what broke.
- Shared eval fixtures live in `scripts/eval-fixtures/` (Maya's profile, resume and a job posting).
- Never put real personal data in skills, examples or evals. Maya Okafor and every company in the
  examples are fictional.
- Skills must save anything they learn to the user's `profile/`, never to files inside a plugin.
