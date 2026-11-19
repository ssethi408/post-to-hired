---
name: "linkedin-post"
description: "Default path for writing any LinkedIn post for the user. Sets the stage, target reader, and reply hook with linkedin-funnel-playbook, drafts in the user's voice from profile/voice.md, runs the-humanizer, then gates the final post against the playbook's five rules. Use whenever the user asks to write, draft, create, or help with a LinkedIn post or LinkedIn content, including \"help me write a post about X\", \"draft something for LinkedIn on Y\", \"turn this into a LinkedIn post\", \"I want to talk about Z on LinkedIn\", or hands over their own draft to finish. Use linkedin-funnel-playbook directly instead when they only want a week planned, a draft checked, gated or diagnosed without a rewrite, or a post for someone other than themselves.\n"
---

# LinkedIn Post Skill v3

Four phases. Phase 0 decides what the post has to do. Phase 1 writes it in the user's voice. Phase 2 makes sure it does not read as AI-written. Phase 3 makes sure Phase 2 did not break what Phase 0 decided.

The goal of every post is engagement on the user's personal account: the right people reading, replying with something of their own, and starting conversations. Posts do not promote an employer's products.

Load the other skills by name with the Skill tool (`linkedin-funnel-playbook`, `the-humanizer`). In a plugin install they may be listed with the plugin prefix (`linkedin-content:linkedin-funnel-playbook`); use the name your skill list shows. Do not hardcode file paths to them. Read the user's voice from `profile/voice.md`; if they have their own voice skill, load that instead.

## Entry points

| The user gives you | Run |
|---|---|
| A topic, idea, news item, or story | Phase 0 → 1 → 2 → 3 |
| Their own finished draft | Phase 0 (stage tag, reader, reply hook only) → 2 → 3. Skip Phase 1. |
| A small edit to a post from this conversation | Make the edit. Re-run Phase 3 only if the edit touched the first paragraph, the first three paragraphs' order, or the closing line. |
| "Run the humanizer again" | Phase 2 → 3 |

---

## Phase 0: Strategy

1. Load `linkedin-funnel-playbook`. Read the user's author profile (`profile/author.md`).
2. **No profile yet:** say so in one line and offer the playbook's SETUP. If they want the post now anyway, state the assumed reader and what they get in one line at the top of the output and carry on.
3. **Pick the stage** (REACH, TEACH, CONVERSATION). Use the one the user names. Otherwise infer it from the topic, say which and why in one line, and check it against the last two posts in the profile (Rule 1).
4. **Pick the reader**: which target reader from the profile this post is for. One per post.
5. **Find the anchor**: the single concrete fact, number, person, or scene the post is built on. Pull it from the proof bank, shareable items only. If nothing fits, ask the user at most two questions. Never invent a detail on their behalf; if they are not available to answer, leave a marked gap. If the anchor involves anything internal to an employer, confirm it is OK to share before drafting.
6. **Write the reply hook**: the one-sentence reply a target reader could post that adds their own experience or view (Rule 5).

Phase 0 produces a five-line brief, shown to the user above the draft:

```
STAGE: <REACH|TEACH|CONVERSATION>   last two: <X, Y | n/a>
READER: <target reader>  ·  gets: <what they get>
ANCHOR: <fact/scene>  [verify if unverified]
REPLY: "<the reply a target reader might leave>"
CLOSE: <story beat | narrow question | comment for resource>
```

---

## Phase 1: Draft in the user's LinkedIn voice

LinkedIn posts are not emails. Carry over only the voice-level rules from `profile/voice.md`. The defaults below apply unless the voice file overrides them:

- No em-dashes
- No emojis
- Direct and concise; cut anything that does not earn its place
- No filler phrases ("Hope this finds you well", "Circling back", "At the end of the day")
- No praise-inflation or hype language

**Structure.** These merge common LinkedIn patterns with the playbook's five rules. Where the voice file and this section disagree on structure, this section wins; on word choice and tone, the voice file wins.

- **Opening paragraph (write it last).** Everything before the first line break, under 210 characters. Open on the anchor: a specific scene, number, person, or event that carries the point. Not a thesis statement on its own, and not a line that only announces a debate or trend. Test: "After reading this you will know/get ___" must fill with a concrete noun from that paragraph. For REACH stories, open on the scene itself, not a general truth about it.
- **Outcome before mechanism.** Say what changed or what is at stake for the reader (time, money, risk, people) before explaining how anything works. For REACH posts the outcome is the human point: what changed for the user or someone in the story.
- **Mechanism in flowing prose.** Not a numbered list, not stacked fragments ("X. Y. Z."). If a sequence needs steps, write it as one sentence: "One thing hits a gap, the next treats it as fact, a third builds on top of it."
- **Plain words up top.** The first two paragraphs use nothing from the user's jargon list and no unexpanded acronyms. Depth and terms of art are fine further down once the reader knows why they care.
- **One concrete example** grounded in the user's actual work. Facts not marked verified get `[verify]`.
- **No reframe punchline** ("X doesn't have a Y problem, it has a Z problem"). State the point plainly.
- **Short paragraphs, varied in length.** Scroll format, not an essay.
- **Close by stage** (this is how the post earns Rule 5):

| Stage | Close with |
|---|---|
| REACH | The story's last beat, or one line on what changed. A question only if it asks for the reader's own version of the moment. |
| TEACH | A narrow question about the reader's own version of the problem ("What did your last reorg do to your release dates?"), not "Thoughts?" |
| CONVERSATION | One explicit, narrow ask: their experience, their position, or "Comment [word] and I'll send the [resource]." Nothing stacked on top of it. |

Never close on a slogan, a summary of the post, engagement bait ("Agree?", "Like if...", "Repost if..."), or a call to act with any company.

Before moving on, check the draft against the five rules yourself and fix what fails. Do not show this draft to the user as finished; Phase 2 and 3 are part of the job.

---

## Phase 2: Humanize

Load `the-humanizer` and run its full Review Pipeline (Steps 1 to 6) on the draft, including Step 6 self-update.

LinkedIn adjustments:

- Treat "bullet-point structure where prose would carry more weight" and the "intro > 3-point list > conclusion" template as hard fails, not soft flags.
- In the Step 5 rewrite, keep these four things fixed: the concrete anchor in the opening paragraph, the outcome-before-mechanism order, the stage close, and the reply hook. Rewrite everything else freely.

---

## Phase 3: Gate

Run the playbook's CHECK mode on the final rewritten post.

- **5/5:** done.
- **Any fail:** apply the smallest fix from the CHECK table, keeping the humanized wording everywhere else. Re-run CHECK once. Do not loop further.
- **If a fix would noticeably change the voice:** show both lines (humanized vs. passing) and let the user pick.
- **Any shareability advisory:** raise it above the post, not buried in the table.

---

## Output

In this order:

1. The Phase 0 brief
2. The final CHECK table, exactly in the playbook's CHECK output format, including the "Smallest fix" column
3. The final post
4. A list of every `[verify]` item and any shareability advisory, if any
5. The humanizer's Structured Review Report (Step 4) and Skill Update note (Step 6), collapsed to the essentials

Save the final post as a markdown file in `posts/` in the working folder (for example `posts/2026-11-18-carrier-onboarding.md`) and send it. The user copies it straight into LinkedIn.

When the user says a post went live, add it with its stage tag to the "last 3 posts" list in `profile/author.md`, so Rule 1 has real history next time. If they share how it did (comments from target readers, DMs, threads), note that too.

## Iteration

Edits, comments, or tweaks after delivery are normal iteration. Do not restart from Phase 0. Re-run Phase 2 only when they ask for another humanizer pass. Re-run Phase 3 under the conditions in the entry-points table.
