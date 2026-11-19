---
name: "pipeline-tracker"
description: "Keep the user's job search pipeline in one place: every lead, application, outreach, interview and follow-up. Adds and updates rows, moves leads through stages, flags follow-ups that are due, and gives a weekly summary. Use when the user says \"add this to my tracker\", \"I applied to X\", \"I heard back from Y\", \"what's due this week\", \"where do things stand\", \"update the tracker\", or when find-hiring-managers, tailor-resume or mock-interview hands over a lead or an update."
---

# Pipeline Tracker

One row per opportunity. Every other skill in `job-search` reads from it or writes to it, so the user always knows what's open, what's waiting on them, and what's gone quiet.

## Where the tracker lives

Read `profile/settings.md` in the working folder you were started in. Never search other folders or the rest of the computer for a profile or tracker; if `profile/` is missing, say so and offer the `setup` skill (it may be listed as `setup:setup`).

Read `TRACKER` from `profile/settings.md`. It can be:

- **A local CSV** (default): `tracker/pipeline.csv` in the working folder. It's gitignored, so it never ends up in a repo.
- **A Google Sheet**, if the user has the Google Sheets connector and gives the sheet's link. Use the same columns.

No tracker yet: create the CSV with the header row below and tell the user where it is.

## Columns

`id, company, role, level, location, source, contact_name, contact_title, link, date_found, fit_score, stage, outreach_status, applied_date, resume_used, interview_dates, last_contact, next_step, next_step_due, notes`

- `source`: LinkedIn post / job board / referral / recruiter / other
- `resume_used`: path to the tailored PDF from `tailor-resume`
- `id`: company plus role plus month, e.g. `acme-product-manager-2026-11`, so the same opportunity never gets two rows

## Stages

`Lead → Contacted → Applied → Screening → Interviewing → Offer → Closed`

`Closed` always gets a reason in `notes`: rejected, withdrew, accepted, or went quiet.

## Customize this

Safe to change: columns (add, never rename an existing one without migrating), stage names, follow-up timing.
Keep: one row per opportunity, the `id` rule, and asking before deleting anything.

## Actions

### Add
Take the fields from the user or from the skill that called you. Check for an existing row with the same `id` first; if there is one, update it instead. Set `next_step` and `next_step_due` for every new row. Confirm the row in one line.

### Update
Find the row by company and role. Change only the fields that moved. When the stage changes, add a dated line to `notes` ("2026-11-18: moved to Screening, recruiter call booked"). Set the next step.

Updates from other skills:
- `tailor-resume` → `resume_used`, and stage `Applied` once the user says they submitted
- `mock-interview` → `interview_dates`, readiness score in `notes`
- `find-hiring-managers` → new rows at stage `Lead` or `Contacted`

### Follow-ups due
Always re-read TRACKER before answering; never answer from memory of the conversation. Give every due date as an actual date with its weekday ("Tue Nov 25"), not "this week" or "next week" alone, and use today's date to decide what is due.

Flag every row where `next_step_due` is today or earlier, and every row stuck in one stage too long. Default timing:

| Stage | Nudge after |
|---|---|
| Contacted (no reply) | 5 business days, then once more after 7; then mark Closed (went quiet) |
| Applied | 7 business days |
| After an interview | 2 business days for a thank-you if none sent, then 5 for a status check |

Offer to draft each follow-up. Use `profile/voice.md` for the wording.

### Weekly summary
Counts by stage, what moved this week, what's due next week, and conversion so far (contacted → reply, applied → screen, screen → interview). Keep it to one table and three lines. End with the single most useful thing to do this week.

## Never

- Delete a row without asking. Closing it is almost always the better move.
- Put the tracker inside a public repo.
- Change a row from another skill's handoff without telling the user what changed.
