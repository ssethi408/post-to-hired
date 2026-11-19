---
name: "setup"
description: "Set up a new user's post-to-hired profile by interviewing them and writing the profile/ files every other skill reads: author.md, voice.md, about-me.md, targets.md, settings.md and, optionally, interview-rubric.md. Pulls what it can from a resume, writing samples or a LinkedIn profile export so the user types as little as possible. Use when the user says \"set me up\", \"set up post-to-hired\", \"create my profile\", \"get started\", \"onboard me\", or when another skill finds no profile/ folder. Also use to update one part later (\"update my voice\", \"change my targets\")."
---

# Setup

Builds the user's `profile/` folder. Every other skill in post-to-hired reads it, so a good profile here is the biggest single improvement to everything else.

## Files bundled with this skill

Paths below are relative to this skill's own folder (the folder this SKILL.md is in), not the user's working folder.

- `templates/`: one blank template per profile file. Write every profile file in the shape of its template.
- `example/maya-okafor/`: a complete profile for a fictional product manager. Show it when the user wants to see what "done" looks like, or load it (see Step 0) so they can try the other skills first.

## Rules

- **Ask in rounds, not all at once.** One round per file, at most 6 questions per round, in one message. Wait for answers before the next round.
- **Pull before you ask.** If the user can give you a resume, writing samples, or their LinkedIn profile (a pasted "About" section, or the PDF from "More → Save to PDF" on their profile), extract everything you can from it first, then ask only for what's missing.
- **Write each file as soon as its round is done**, show it, and ask "Anything to change?" before moving on. Partial setup is useful; the user can stop at any time.
- **Never invent.** Leave a blank or `[TODO: ...]` where you don't have an answer.
- **Everything is private by default.** See the privacy check at the end.

## Step 0: Where and how much

Ask in one message:

1. **Working folder.** "Which folder will you start Claude in for your job search?" Default: the current folder. The profile goes in `profile/` inside it.
2. **What they'll use:** LinkedIn posts, resume tailoring, hiring-manager outreach and tracking, mock interviews. Skip rounds for parts they won't use.
3. **Quick or full.** Quick (about 10 minutes): the minimum each skill needs. Full (about 30 minutes): richer stories and voice, better output from day one.
4. **What they can share up front:** resume file, 2 or 3 posts or emails they wrote, their LinkedIn About section or profile PDF.
5. **Or try the example first?** Load the fictional Maya Okafor profile so they can test the other skills right away and set up their own later.

**Loading the example:** copy every `.md` file from `example/maya-okafor/` except `README.md` into `profile/` in the working folder. Copy each one with Read and Write rather than shell commands, so it works the same everywhere and needs no shell permission. Then add this first line to each copied file: `<!-- EXAMPLE PROFILE: fictional. Run setup again to replace it with your own. -->`. Tell the user the profile is fictional and that any skill they run will write as Maya until they replace it. Resume tailoring and mock interviews also need a real resume: Maya's `example/maya-okafor/settings.md` points to a file that doesn't exist, so the user should set RESUME_SOURCE in `profile/settings.md` before trying those. When they later run setup for real, treat files that still have that first line as safe to replace, and say so before replacing them.

If `profile/` already exists, read it, list which files are present, which have `[TODO]`s, and which are still the example profile, and offer to fill only the gaps. Never overwrite a file without asking.

## Round 1: targets.md (job search, tailoring, mock interviews)

Pull from the resume first: current title, level, industry, location.

Ask:
1. What roles and titles are you going for? Any you'd rule out?
2. What level: individual contributor, manager, director, executive?
3. Which industries or kinds of company (size, stage)?
4. Location and remote preference?
5. Compensation floor? (Optional. Say it's only used to flag mismatches and never leaves their computer.)
6. Dealbreakers, and any dream companies?

Write `profile/targets.md` in the shape of `templates/targets.md`.

## Round 2: settings.md (tailoring and tracker)

Ask:
1. Where is your master resume? (Path to a .docx. If they only have a PDF, say tailoring works best from a .docx and offer to continue with what they have.)
2. Where should tailored resumes go? Default: `~/Documents/Resumes`.
3. What should every tailored PDF be called? Suggest `Firstname_Lastname_Resume.pdf`.
4. How many pages? Default 2 for 10+ years of experience, otherwise 1.
5. Tracker: a local CSV (default `tracker/pipeline.csv`) or a Google Sheet (paste the link)?

Write `profile/settings.md` in the shape of `templates/settings.md`. If they chose a CSV, offer to create it with this header row (the same columns the pipeline-tracker skill uses):

```
id,company,role,level,location,source,contact_name,contact_title,link,date_found,fit_score,stage,outreach_status,applied_date,resume_used,interview_dates,last_contact,next_step,next_step_due,notes
```

## Round 3: about-me.md (stories, used everywhere)

Pull from the resume first: draft a 3 to 5 line career summary and list the 4 to 6 results on it that could become stories.

Then ask (quick mode: just 1 and 2; full mode: all):
1. Here's the summary I drafted. What's wrong or missing?
2. Pick 3 of these results. For each: what was the situation, what did *you* do, what was the result, what did you learn?
3. A time something went wrong and what you did about it.
4. A disagreement with a manager or stakeholder and how it ended.
5. A decision you made without enough information.
6. Anything you're proud of that isn't on the resume.

Write `profile/about-me.md` in the shape of `templates/about-me.md`, each story in the template's format, with the question types it's good for. Mark anything internal to an employer (customer names, internal numbers) as `[private: interview only]`. Those can be told in an interview but not posted.

## Round 4: voice.md (posts, outreach, rewrites)

Best input: 2 or 3 things they wrote themselves (posts, emails, a doc). Analyze those first: sentence length, how they open, how they close, words they use often, punctuation habits, lists vs. prose. Show your read in 5 lines and ask if it's right.

Then ask:
1. Describe how you want to sound in three words.
2. Words or phrases that make you cringe?
3. How do you open a post: story, number, opinion, question?
4. How do you end one?
5. Emojis, em-dashes, hashtags: yes or no?
6. "I" or "we" when talking about team work?

Write `profile/voice.md` in the shape of `templates/voice.md`. Put their own samples in the Samples section only after checking them for private details with the user.

## Round 5: author.md (LinkedIn only)

This is the linkedin-funnel-playbook's SETUP, run here so the user does it once. Ask the playbook's five questions:

1. Who do you want engaging with your posts? 2 or 3 reader types: role, context, what they're working through.
2. What does each reader type get from following you, in their words?
3. What does good engagement look like at 90 days (give a number) and at 1 year?
4. Proof bank: build it from `profile/about-me.md`, then ask the user to mark each item verified or unverified, and shareable or not. Employer-internal items default to not shareable.
5. Jargon: 10 to 15 words from their field a stranger wouldn't know.

Also ask: 2 or 3 topics to be known for, follower count, how often they post now, target posts per week, how long they'll give a change before judging it, and their last 3 posts if they have any.

Write `profile/author.md` in the shape of `templates/author.md`.

## Round 6 (optional): interview-rubric.md

Only if they use mock interviews and their field has its own bar. Ask: "What does a great answer look like in your field that a general interviewer might miss?" Turn the answer into 1 to 3 extra rubric rows and write `profile/interview-rubric.md` in the shape of `templates/interview-rubric.md`.

## Privacy check (always, before finishing)

1. List every file written, as a short table: file / status.
2. Check where `profile/` lives. If it's inside a git repository, check that `.gitignore` covers `profile/`, `tracker/` and `posts/` (where linkedin-post saves drafts). If not, add those lines and say so. If the folder is inside a public repo the user doesn't control, warn them and suggest moving it.
3. Scan the files for anything that looks like a home address, phone number, personal email, account number, or someone else's private details (family, colleagues' performance). Ask the user whether each should stay.
4. Remind them in one line: "Everything in profile/ stays on this computer. Nothing here is committed or shared unless you do it yourself."

## Finish

Show a short table: file / status (done, partial, skipped) / what's still `[TODO]`. Then suggest the first thing to try, based on what they set up:

- LinkedIn: "Help me write a post about [a story from about-me.md]."
- Resume: "Here's a job posting, tailor my resume for it."
- Outreach: "Here's a hiring manager's post. Is it a fit?"
- Interview: "Run a mock interview for [role] at [company]."

## Updating later

"Update my voice", "add a story", "change my targets": open just that file, show what's there, ask only about the part that's changing, and show the edit before saving.
