---
name: "find-hiring-managers"
description: "Turn LinkedIn posts and job listings the user finds into qualified leads: hiring managers who are hiring for roles that match the user's targets. Qualifies each lead against profile/targets.md, researches the role and company from public sources, drafts a short personal outreach note in the user's voice, and adds the lead to the pipeline tracker. Use when the user pastes a LinkedIn post like \"I'm hiring a...\" or \"my team is growing\", shares a job listing and asks who the hiring manager is, or asks to qualify leads, draft outreach to a hiring manager, or plan this week's outreach."
---

# Find Hiring Managers

Hiring managers who post about open roles are often the shortest path to an interview. This skill helps the user qualify those leads, research them, and write outreach worth answering. Then it hands every lead to `pipeline-tracker`.

## What this skill does not do

The user finds the posts and sends the messages. This skill does not log into LinkedIn, scrape it, send connection requests or messages, or automate the user's account. LinkedIn's user agreement prohibits those, and they can get an account restricted. If the user asks for any of them, say so in one line and offer the manual version instead.

## Customize this

Safe to change: the qualification criteria (they come from `profile/targets.md`), the score threshold, the outreach length, the search phrases below.
Keep: never invent a connection or shared history, never send anything for the user, one lead per tracker row.

## Mode 1: Search plan

When the user asks where to look, give them search phrases to paste into LinkedIn's own search (Posts, sorted by latest), built from the roles and industries in `profile/targets.md`:

- `"hiring" "[role title]"`, `"my team is hiring" [function]`, `"we're looking for" "[role title]"`
- `"join my team" [function]`, `"open role" [function] [location or "remote"]`
- Ask them to filter by "Past week" so leads are fresh.

Tell them to paste each promising post (or the post's text plus the poster's name, title and company) back into the chat.

## Mode 2: Qualify

Read `profile/targets.md`, `profile/voice.md` and `profile/about-me.md` from the working folder you were started in. Never search other folders or the rest of the computer for a profile. If `profile/` is missing, say so and offer the `setup` skill (it may be listed as `setup:setup`).

For each post or listing the user pastes:

1. **Extract:** poster name, poster title, company, role being hired, level, location / remote, the date posted, and any link to a job listing.
2. **Is the poster the hiring manager?** Yes if they say it's their team or they'd be the manager. Recruiter or someone sharing for a colleague: still a lead, but note who the likely hiring manager is if the post says so.
3. **Score fit** against `profile/targets.md`, 1 to 5 on each:
   - Role match (title and function)
   - Level match
   - Location and remote match
   - Industry or company match
   - Dealbreakers: any hit means the lead is marked **Pass** no matter the score
4. **Research from public sources only:** what the company does, size and stage, recent news, the job listing if there is one. Cite URLs. If the user has a tailored resume for a similar role, note which one.
5. **Verdict:** Pursue (total 16 or more, no dealbreakers), Maybe (12 to 15), or Pass. One line on why.

Output a table, one row per lead: poster / company / role / fit score / verdict / why.

## Mode 3: Outreach

For each lead marked Pursue, or any lead the user picks:

1. Read `profile/voice.md` and `profile/about-me.md`.
2. Find the one true, specific link between the user's experience and what the poster said they need. Quote the post's own words back. If there is no real link, say so rather than forcing one.
3. Draft two versions:
   - **Connection note:** under 300 characters, the length LinkedIn allows on a connection request.
   - **Message:** 3 to 5 sentences. What caught their eye in the post, the one relevant result from their own work, a clear and easy ask (a 15-minute call, or "who's the best person to send my resume to").
4. Rules: no flattery, no "I came across your post", no attachments in the first message, no em-dashes, no invented mutual connections or shared history. Use their first name.
5. Show both drafts. The user edits and sends them.

## Mode 4: Hand off to the tracker

After qualifying or drafting, ask: "Add these to the tracker?" On yes, load the `pipeline-tracker` skill (it may be listed as `job-search:pipeline-tracker`) and pass each lead's fields: company, role, poster name and title, post link, date found, fit score, verdict, outreach status (Drafted / Sent), and next step.

## Never

- Send, connect, or post anything on the user's behalf.
- Scrape LinkedIn or ask the user for their LinkedIn password or cookies.
- Guess personal details (emails, phone numbers) for a poster. If the user wants an email address, point them to the company's public careers or contact page.
- Invent a connection, a shared employer, or a result the user didn't have.
