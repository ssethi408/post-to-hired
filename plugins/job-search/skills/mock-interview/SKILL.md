---
name: "mock-interview"
description: "Run a realistic mock interview with the user for a specific upcoming interview, then debrief it. Researches the company and role first, asks one question at a time in the chosen interviewer style, follows up on vague answers, and scores every answer at the end with rewrites in the user's voice. Use when the user says they have an interview coming up and wants to practice, asks for a mock interview, interview prep, \"grill me\", \"practice the hiring manager round\", or \"prep me for my interview at X\"."
---

# Mock Interview

Three phases: **Prep** (an agent builds the brief), **Interview** (you run it live, one question at a time), **Debrief** (an agent scores the transcript). The interview runs here in the main conversation because subagents cannot talk to the user turn by turn.

**Interviewer styles** come from two places. Read both and treat them the same:
- `interviewer-styles/` in this skill's own folder: the four that ship with post-to-hired.
- `profile/interviewer-styles/` in the user's working folder: styles the user added. If both have a file with the same name, the user's wins.

New styles are always saved to `profile/interviewer-styles/`, never to this skill's folder, which a plugin update replaces.

**The two agents** ship in the job-search plugin as `interview-researcher` and `interview-debrief`. In a plugin install their names may carry the plugin prefix (`job-search:interview-researcher`); use whichever name your agent list shows. If agents are not available, do the agent's work yourself by following its instructions in `../../agents/<name>.md` relative to this skill's folder, then continue.

## Customize this

Safe to change: interviewer styles (add your own in `profile/interviewer-styles/`), question counts, the rubric in `profile/interview-rubric.md`.
Keep: one question per turn, no feedback during the interview, no invented facts about the user in rewrites.

## Phase 0: Setup

Read `profile/` from the working folder you were started in; never search other folders for a profile. If it's missing, offer the `setup` skill.

Ask in one message, skipping anything already known from the conversation or the tracker:

1. **Company and role.** If the tracker or `APPLICATIONS_ROOT` (from `profile/settings.md`) has a folder for this role, use its job description and tailored resume. Otherwise ask for the job posting (URL or pasted text).
2. **Stage:** recruiter screen, hiring manager, technical / craft, panel, or final / executive. Map it to a style file (see above). Technical and final rounds have no shipped file: start from the closest one (hiring manager for technical, skeptical bar-raiser for final) and adapt. If the user describes a style that has no file, improvise it from their description and offer afterwards to save it as `profile/interviewer-styles/<name>.md`, in the same format as the shipped files.
3. **Interviewer**, if known: name, title, and anything public about them (the user can paste a LinkedIn summary). Use only what they give you or what is public.
4. **Length:** short (5 questions, about 15 minutes), standard (8, about 30), or full (12, about 45). Default to standard.
5. **Date of the real interview**, for the tracker.

## Phase 1: Prep

The agents can read text files but not `.docx` or `.pdf`. Before launching either agent, extract the resume's text (pandoc, python-docx, or the PDF's text layer), save it to a temporary `.txt` or `.md` file outside the user's profile and applications folders, and pass that path. If you can't extract it, ask the user to paste the resume text.

Launch the `interview-researcher` agent with: the job description, the tailored resume (or master resume from `profile/settings.md`), the paths to `profile/about-me.md` and `profile/targets.md` if they exist, the stage, the interviewer details, and the question count.

It returns a brief: what the role really needs, resume gaps an interviewer will probe, likely questions, and the user's best story for each.

Show the user a short version: the 3 things this interviewer most needs to hear and the 2 gaps most likely to be probed. **Do not show the question list.** Ask: "Ready to start, or want to look at anything first?" If they want to see the questions, show them, and warn that practice is less realistic once they have seen them.

## Phase 2: Interview

Read the style file and stay in that interviewer's voice for the whole interview.

**Facts about the company, team and role come only from the job posting, the prep brief (which cites its sources) and what the user told you.** Do not invent team size, headcount, org structure, strategy, problems, products or anything else to make the interviewer sound real. If the interviewer would naturally share context you don't have, keep it general ("we're growing the carrier side") or skip it. The debrief must not build on anything the interviewer said that isn't in those sources.

- Open the way that interviewer would: a short intro, then the first question.
- **One question per turn.** Wait for the answer.
- **Follow up** when an answer is vague, all "we" with no "I", has no result, or dodges the question. At most 2 follow-ups per question, then move on. Follow-ups are how the user learns where real interviewers will push.
- **No feedback, coaching, or praise during the interview.** A neutral "Thanks" or "Got it" is fine. Hold all evaluation for the debrief.
- Go after the gaps from the brief at least once, the way a real interviewer would.
- Commands from the user at any time:
  - `pause`: stop and wait until they say `resume`
  - `hint`: one-line nudge on what this question is really testing, then continue
  - `redo`: they want to answer the last question again; take the new answer
  - `end`: stop and go to the debrief
- Close the way that interviewer would, including "What questions do you have for me?" Answer as the interviewer, using only what is in the brief or the job posting. If you do not know, say "That's a good one for the hiring manager."

Keep a clean transcript as you go: each question, each follow-up, and the user's answers word for word.

**Speaking practice:** if the user says they are answering out loud (dictation or voice mode), allow filler words and rambling in the transcript; the debrief scores delivery too.

## Phase 3: Debrief

Launch the `interview-debrief` agent with: the transcript, the brief, the style file name, the resume used, and the paths to `profile/voice.md`, `profile/about-me.md` and `profile/interview-rubric.md` if they exist.

Show the user, in this order:

1. **Readiness:** a 1 to 10 score and one sentence on what would move it up.
2. **Per-answer scorecard:** a table with one row per answer and one column per rubric dimension (each scored 1 to 5), then a total. Don't collapse it into a single score per answer.
3. **The 2 to 3 weakest answers rewritten** in the user's voice, using only facts from the transcript, the resume, or `profile/about-me.md`. Gaps get `[ADD: specific number or example]`, never an invented fact.
4. **Resume consistency:** anything said that contradicts or goes beyond the resume.
5. **Stories to save:** new stories from the answers worth adding to `profile/about-me.md`. Ask before writing them.
6. **Next practice round:** the one question type to drill next.

## Phase 4: Save

After the user approves:

- Write `prep-brief.md` and `debrief-{YYYY-MM-DD}.md` into the role's folder: `APPLICATIONS_ROOT/{Company}/{Role} - {YYYY-MM}/interview/`. If there is no role folder, ask where to save.
- Add the approved stories to `profile/about-me.md`.
- If a tracker exists, update this role: interview date, stage, readiness score, date of the mock.

## Never

- Invent experience, numbers, or employers for the user, in the interview or in rewrites.
- Coach during the interview.
- Ask more than one question per turn.
- Claim to know private facts about the interviewer or company. Public information and what the user gives you only.
