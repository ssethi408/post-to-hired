---
name: "linkedin-funnel-playbook"
description: "Plan, check, and set up LinkedIn posts for a personal account built on engagement, not company sales: the right people reading, replying, and starting conversations. Three stages (REACH, TEACH, CONVERSATION) and five rules. Set up an author profile once, plan a week of posts, gate a draft against the five rules, or diagnose why a post underperformed. Use when someone asks to plan LinkedIn content, check or gate a post (\"is this ready\", \"gate this\", \"funnel check\"), diagnose a post that flopped or underperformed (\"why did my post flop\"), set up an author, or write a post for someone else. When the user wants their own post written or finished, linkedin-post calls this skill; do not trigger it directly for that. Checking, gating, diagnosing or planning their posts does trigger it directly. Not a voice skill: run the author's own voice skill or guide, if one exists, and the-humanizer after this.\n"
---

# LinkedIn Engagement Playbook v2.2

One method, three stages, five rules. The goal is engagement on a personal account: the right people reading, replying with something of their own, and starting conversations. It is not a funnel for the author's employer or any company's product.

Nothing author-specific lives in this file; that goes in the author profile.

## Modes

Pick the mode from what the user asked. Say which mode you are in, in one line.

| Mode | User says | You produce |
|---|---|---|
| **SETUP** | "set up [name] for LinkedIn", first use for a new author | `profile/author.md` (or `profile/authors/<name>.md` for someone else) filled from the questions below |
| **PLAN** | "plan this week", "what should [name] post" | 3 post slots with stage, angle, and source material |
| **DRAFT** | "write a [REACH/TEACH/CONVERSATION] post for [name] about X", or called by an author's own post skill | One post, stage-tagged, passing the five rules |
| **CHECK** | "gate this", "is this ready", "why did this flop", pastes a draft | The 5-rule table below, smallest fix per fail |

## SETUP: the author profile

The method needs context it cannot invent. Ask these once, save the answers, reuse every time. Interview style, 5 questions, one message.

1. **Who do you want engaging?** Two to three reader types: role, context, and what they are working through. These are the people whose comments and DMs count. Everyone else is reach.
2. **What do they get from following you?** For each reader type, in their words: the thing they want to be better at, avoid, or understand. Not your credentials.
3. **What does good engagement look like at 90 days and 1 year?** Comments per post from target readers, conversations or DMs a month that turned into something real (a call, an intro, a collaboration), connections of the right kind. Get a number for the 90-day one.
4. **Proof bank.** Every fact and story you are allowed to use: career moves, programs you ran, mistakes, people who shaped you, numbers you can stand behind. Mark each **verified** or **unverified**, and **shareable** or **not shareable**. Anything internal to a current or past employer (unreleased plans, customer names, internal numbers, people's performance) defaults to not shareable until the author says otherwise.
5. **Voice constraints and jargon list.** Is there a voice skill or guide? Banned words, banned formats, how they say "I" vs "we". Then 10 to 15 words from the author's field that a stranger would not know. Rule 4 tests against this list.

Also record: 2 to 3 topics the author wants to be known for, current follower count, posting cadence today, target cadence (posts per week), how long they will give a change before judging it, and last 3 posts with stage tags.

Profile template is at `profile-template/author.md` in the post-to-hired repo.

No profile yet and the user wants a CHECK or DRAFT now: state the assumed reader and what they get in one line at the top of the output, proceed, and offer SETUP at the end.

## The stages

Three stages, each with a different job and a different metric. A post that tries to do all three jobs at once usually does none of them.

### REACH

- **Job:** get the author in front of many people as a person worth following. Most of the audience will not be target readers, and that is fine.
- **Post types:** the author as a person. A decision they made and what it cost, something they got wrong, a job change or other transition, a person who changed how they work. Observations about the author's field that describe a change without prescribing a fix.
- **Metric:** impressions, follower growth, reactions moving from tens to hundreds.

### TEACH

- **Job:** leave the target reader understanding a problem in their own work better than they did before reading.
- **Post types:** a problem the reader has, broken down with the author's own example. A lesson from the author's work, with the numbers or details that make it credible. A recent change in the reader's field and what it means for their day-to-day.
- **Source:** the proof bank first; then whatever the target readers are dealing with this month.
- **Metric:** substantive comments from target readers, saves, reposts, inbound DMs.

### CONVERSATION

- **Job:** get target readers to respond with something of their own. No company, product, or offering is promoted.
- **Post types:**
  - **Ask for their version.** The author shares a specific experience, then asks readers for theirs. The ask is narrow enough that a one-line answer is easy.
  - **A considered position.** A real stance the author holds, with the reasoning, that thoughtful people could disagree with. Not contrarian for its own sake.
  - **A free resource:** a template, checklist, or framework the author made. "Comment [word] and I'll send it." The resource is the point; nothing is sold behind it.
  - **A call for input** on something the author is actually working through.
- **Metric:** comments from target readers, replies-to-replies (threads), DMs, connection requests from the right people.
- **Weight:** earn it. Asking an audience that does not know you yet reads as engagement bait.

### Cadence and signal

- Posts per week: use the target cadence in the author profile. If there is none, ask; do not assume one.
- Mix: mostly REACH and TEACH in the first 90 days, CONVERSATION at most once a week. Treat this as a starting point and adjust once the author's own results say otherwise.
- Leading indicator: who is engaging (target readers or not), not how many. Follower count is lagging. Judge a change only after the review window in the author profile.
- Reply to every substantive comment within the first few hours, with something more than thanks. A reply that adds a detail or asks a follow-up is what turns a comment into a thread.

## The five rules

Every post at every stage. Each has a mechanical test. Use these when drafting and in CHECK mode.

### Rule 1: Right stage for this week

Tag the post. CONVERSATION if the post's main job is to get readers to respond (a direct ask for their experience or view, a comment-for-resource offer, a call for input). TEACH if it explains a reader problem or a change in their world and says what should be done or how. Else REACH.

Check against the last two shipped posts; planned slots earlier in the same week count. Unknown: write "n/a" and pass. FAIL if all three would be CONVERSATION (asking before giving). Flag two CONVERSATION in a row as a note.

Separately, flag (not fail) any post that names or promotes the author's employer's product or asks readers to act with a company. That is outside this playbook's purpose; the author decides.

### Rule 2: First paragraph tells the reader what they get

"First paragraph" = text before the first line break, cut at 210 characters (what shows before "...more").

Test: fill "After reading this you will know/get ___" using a concrete noun from the paragraph. Concrete = a number, a proper noun, a job title, a date, or a physical thing or event. Abstract nouns (nuance, debate, moment, shift, future, journey, innovation) do not fill it. FAIL if it cannot be filled. FAIL if the blank is about a company or product rather than the reader or the author as a person.

A first line that only announces a debate, problem, or trend exists ("the debate over X misses the nuance") FAILS. A known analogy or comparison passes if the paragraph says who or which field it applies to.

REACH stories: a specific scene (a person plus a moment: "Last Tuesday my mom called and asked what my job really is") fills the blank. A general truth about the scene ("Moms know how to make you question your life choices") does not; cut it and open on the scene.

### Rule 3: Outcome before mechanism

Outcome sentence = names what the reader gets (from the author profile) or a specific person's result in time, money, risk, or people. Negative results count. Mechanism sentence = says how something works, what a process or tool does, or what the author did step by step. FAIL if a mechanism sentence comes before the first outcome sentence and no outcome sentence appears within the first 3 paragraphs or 500 characters, whichever is longer. Depth is welcome after the reader knows why they care.

For REACH posts, "outcome" means the human point of the story (what changed for the author or someone in it).

### Rule 4: Stranger test

Reader: the primary target reader from the author profile, who has never heard of the author and does not work in the author's field.

Test: write "This post says ___, and it matters to me because ___" using only content words from the first two paragraphs plus function words. FAIL if it needs a word on the author's jargon list, an unexpanded acronym, a proper noun other than the author's name, or a word not in those paragraphs. FAIL if the second blank cannot be filled. No profile: treat acronyms and unknown proper nouns as jargon.

### Rule 5: Something to reply to

Test: write the one-sentence reply a target reader could post that adds their own experience, opinion, or question. FAIL if the only possible reply is agreement or praise ("So true", "Great post"). FAIL on engagement bait: "Agree?", "Thoughts?", "Like if...", "Comment YES", "Repost if...", or any ask that a reader could answer without having read the post.

REACH posts pass with an implicit opening (a story a reader can match with their own); they do not need a question. CONVERSATION posts must make the ask explicit and narrow.

### CHECK output

```
STAGE: <REACH|TEACH|CONVERSATION>   last two: <X, Y>
RULES: <n>/5 pass

| # | Rule | Result | Why (one line) | Smallest fix (one line) |
|---|------|--------|----------------|--------------------------|
```

Then, only on fails, max 3 sentences on what to fix first. Do not rewrite unless asked. Add one advisory line if the post closes on a slogan (a last line with no person, number, or mechanism in it); cold readers drop off there. Add one advisory line if the post uses a proof-bank item marked not shareable, or an employer-internal detail not in the proof bank.

For "why did this flop": run CHECK as above. If all five pass, say so and name the likelier causes outside the rules (wrong stage for the week, wrong reader, no replies from the author in the first hours, posting time), without guessing at numbers you were not given.

## DRAFT workflow

1. Confirm the author profile exists. If not, run SETUP first.
2. Take the stage from the user or from PLAN. Say it.
3. Gather raw material from the proof bank (shareable items only) and, if thin, ask the author two interview questions max. No author available: invent nothing; leave the slot as an interview question.
4. Write the first paragraph last. Draft the body, find the sentence that would make the target reader stop scrolling, and move it to the top.
5. Run the five rules on your own draft. Fix fails. Show the table.
6. Flag every fact not marked verified with [verify].
7. Hand off: author voice skill, then the-humanizer. If a post skill called this one (for example linkedin-post), return the stage, reader, anchor, and reply hook to it and let it run the rest.

## PLAN workflow

For the week: one slot per post in the author's target cadence. For each, give stage, one-line angle, the source (proof-bank item, news item, or interview question to ask), and the reply a target reader is likely to leave. Apply the cadence mix and say it is a starting point. Tie each slot to one of the author's 2 to 3 topics.

## Calibration

`references/calibration-posts.md` (optional, create it as you go) holds real posts with expected results for the five rules. Re-run them after editing this file. Add a post for each author as results come in.

v2.1 (2026-10-28): engagement-focused version for personal accounts. Calibration set started with one real post.
v2.2 (2026-11-18): cadence and review window moved into the author profile; stage descriptions rewritten; Rule 3 renamed.
