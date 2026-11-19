---
name: "hiring-manager-outreach"
description: "Write a short, personal LinkedIn message to a hiring manager about a role they posted. Checks how the user is connected to that person first (mutual connections, shared school or employer), opens with that link, and matches the user's real results to the posting's top requirements, in the user's own voice. Use when the user asks to write, draft, rewrite or improve a message to a hiring manager or someone who posted a job, or when find-hiring-managers hands a lead over for outreach."
---

# Hiring Manager Outreach

A cold message gets read when it starts with something the two people actually share and then shows, in one or two real results, why the sender fits this exact role. This skill writes that message. It doesn't send anything.

## What this skill does not do

The user reads LinkedIn and sends the messages. This skill does not log into LinkedIn, scrape profiles, send connection requests or messages, or guess anyone's email address. If the user asks for any of that, say so in one line and offer the manual version.

## Customize this

Safe to change: the message length, the greeting and sign-off (they come from `profile/voice.md`), the question ideas in Step 4.
Keep: check the connection before writing, never invent a connection or an overlap, never mention gaps in the message, never send anything.

## Step 1: Gather what you need

Read from the working folder you were started in (never search other folders or the rest of the computer for a profile):
- `profile/about-me.md`: the user's schools, employers (with dates where known) and stories with real numbers.
- `profile/voice.md`: how they write, and any greeting, sign-off or phrases they always or never use.
- `profile/targets.md`: the level and roles they're aiming for.
- `profile/outreach-examples.md` if it exists: messages the user actually sent and liked. Match their style.

If `profile/` is missing, say so and offer the `setup` skill (it may be listed as `setup:setup`).

From the user, get:
1. **The post:** the hiring manager's name, title, company and what they wrote.
2. **The job posting** if there is one. If it's a public URL, fetch it and pull out the role's real focus (it can differ from the post), its 2 or 3 most important requirements, location and pay if listed.
3. **How they're connected.** If the user hasn't given it, ask once, and say exactly what to copy from the hiring manager's LinkedIn profile:
   - the "mutual connections" line (who the shared connections are),
   - anything under "Highlights" (for example "You both studied at ..." or "You both worked at ..."),
   - the Education and Experience sections (schools, employers and years).
   If the user says there's nothing in common, take their word for it and move on.

## Step 2: Work out the connection

Compare what the user pasted with `profile/about-me.md`:
- **Mutual connections:** list them by name. If the user says one of them is a close friend or a former teammate, note it.
- **Shared school:** same school, and whether their years overlapped.
- **Shared employer:** same company, and whether their dates overlapped. If either side's dates are missing, don't claim they worked there at the same time; the message can ask instead.

Write it as one or two plain sentences under **How you're connected**, for example: "Mutual connection: Dev Kapoor. You both worked at Quillmoor Freight, but not at the same time (she left in 2019, you joined in 2020)." If there's nothing, say "No mutual connections, school or employer in common."

## Step 3: Warm intro

If there are mutual connections, name the best one to ask (a close friend first, then anyone who works at the hiring company), and draft a one-line ask in the user's voice, for example: "Hey Dev! Priya Raman is hiring a Director of Product at Fernwick. Do you know her? Would you be open to a quick intro or putting in a good word?" If there's nobody, say "Cold message only."

## Step 4: Draft the message

Structure, with a short paragraph per part:
1. **Greeting and opener:** first name, a friendly line, and the role in the post's own words. Use the greeting and sign-off from `profile/voice.md` when it names them.
2. **Connection line,** only if Step 2 found something real: name it and ask one light, friendly question about it ("Looks like we both know Dev Kapoor. How do you two know each other?", "I noticed you were at Quillmoor too. What team were you on?"). Skip this part when there's no real link.
3. **Proof paragraph:** take the posting's 2 or 3 most important requirements and give one specific, true result with its number for each, then one short line that translates it into the posting's terms ("That's basically carrier onboarding with a payments bent."). If the user once worked at the same kind of company as the hiring company, that can be one of the proof points.
4. **The ask:** a quick intro call, plus an offer to send a resume.
5. **Sign-off.**

Rules:
- **Vary the lead.** Don't open with the user's job title, team size or the same headline result every time. Pick the proof that fits this posting.
- Use only facts from `profile/about-me.md`, the user's resume or what the user said in this conversation. No flattery, no "I came across your post", no em-dashes. Don't mention gaps.
- 150 words or fewer. Casual and warm, the way the user actually talks, not a resume summary.
- Also draft a **connection-request note** under 300 characters, the most LinkedIn allows, for when they aren't connected yet.

## Step 5: Show the drafts

Show, in this order: **How you're connected**, **Warm intro** (who to ask and the one-line ask), the **message**, the **connection note**. The user edits and sends them.

If the user shares a message they actually sent and liked, ask whether to save it to `profile/outreach-examples.md` so future drafts match it. Save only on yes, and only there.

If the `pipeline-tracker` skill is available (it may be listed as `job-search:pipeline-tracker`), ask whether to add or update the lead, with the connection and warm-intro contact in its notes.

## Never

- Send, connect, or post anything on the user's behalf.
- Scrape LinkedIn or ask for the user's LinkedIn password or cookies.
- Invent a mutual connection, a shared school or employer, an overlap in dates, or a result the user didn't have.
- Save anything outside the user's `profile/` or tracker.
