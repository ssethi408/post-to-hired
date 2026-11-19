---
name: "karpathy-post-review"
description: "Review the user's LinkedIn posts against the four Karpathy guidelines (think first, simplicity, surgical edits, goal-driven), with line-level findings and minimal fixes."
---

# Karpathy Post Review

A review lens for LinkedIn posts, adapted from the "Karpathy Guidelines" (the community CLAUDE.md by Forrest Chang at github.com/forrestchang/andrej-karpathy-skills, MIT, distilled from Andrej Karpathy's posts on how LLMs fail when coding). The original four principles are about code. This skill maps each one onto writing a post.

Original spirit, kept intact: **caution over speed. Doing less, correctly, beats doing more and overshooting.** For a two-line post, use judgment and don't run the full ceremony.

## When to use

- The user pastes one or more LinkedIn posts (drafts or already published) and asks to run them through Karpathy, check them, tighten them, or "karpathy this".
- Several posts at once: review each separately, then add a short cross-post pattern section at the end.

Before reviewing, open `profile/author.md` and `profile/voice.md` in the working folder you were started in with the Read tool. Don't conclude they're missing without trying to read them; only if the Read fails, say so in one line and infer the reader. They tell you who the author's readers are, which jargon those readers already know, and how the author writes, so you don't flag terms the target reader uses every day or rewrite away the author's style.

This is a review, not a rewrite. If they want a new post written, that is the linkedin-post skill's job. If they want funnel-stage or reach diagnosis, pair with linkedin-funnel-playbook. This skill can run before or after either.

## The four principles, translated for posts

### 1. Think Before Writing
Code version: don't assume, don't hide confusion, surface tradeoffs.

Check:
- Can the post's single point be stated in one sentence? Write that sentence. If you can't, that is finding #1.
- Who is the reader? Name the specific person this is for. If the post reads as written for everyone, flag it.
- Hidden assumptions: claims that rely on context the reader doesn't have (internal jargon, unexplained acronyms, "we" with no referent, a situation that isn't set up).
- Multiple readings: if a line or the whole post can be read two ways (humblebrag vs. lesson, complaint vs. insight), present both readings. Don't silently pick one.
- Vagueness hiding fuzzy thinking: "alignment", "impact", "leverage", "transformation" with nothing concrete behind them.
- If you are unsure what they meant, say so and ask. Don't guess and polish the guess.

### 2. Simplicity First
Code version: minimum code that solves the problem, nothing speculative.

Check:
- Every sentence must serve the one point. Tangents, second ideas, and "also..." paragraphs get flagged for cutting (they may be their own post).
- No scaffolding for a single idea: a "5 lessons" listicle around one real lesson, a framework with a name invented for one example, headers in a 150-word post.
- No speculative padding: hedges, throat-clearing openers, restating the point at the end, generic closing questions added "for engagement".
- Length test: if 300 words could be 120, say so and show which lines go.
- The senior-reader test: would a sharp exec scrolling past say "this is overwritten"? If yes, simplify.

### 3. Surgical Changes
Code version: touch only what you must, match existing style, every changed line traces to the request.

This governs how you edit, not what you check:
- Change only lines tied to a finding. Don't reword lines that already work.
- Keep the author's voice, rhythm, and word choices (see `profile/voice.md` if it exists). Don't swap their phrasing for your own preferences.
- Every suggested edit must point to the principle and finding it fixes. No untraceable "improvements".
- If something looks off but outside the brief (a factual claim you can't verify, a tone risk, a name or company mention), flag it. Don't silently change it.
- If your own cut leaves a dangling reference or a broken transition, fix that orphan too, and only that.
- No em-dashes in any line you suggest.

### 4. Goal-Driven Execution
Code version: turn vague tasks into verifiable goals, then loop until they pass.

Check:
- What is this post supposed to make happen? Name one verifiable goal: e.g. a specific type of reader replies with their own experience, a hiring manager DMs, a peer debates the claim. "Engagement" or "visibility" is not a goal.
- Does the hook (first two lines, before "see more") give the target reader a reason to expand?
- Does the ending give that reader something specific to respond to? A generic closing question ("Thoughts?", "Agree?", "What do you think?") always gets its own finding, with a narrower question as the fix.
- Verify: re-read the post as the target reader. Does every line move them toward the goal? List the lines that don't.

## Output format

For each post:

**Post [n]: "[first ~8 words]..."**

- **The point, in one sentence:** [your sentence, or "Couldn't find one"]
- **Reader and goal:** [who] / [what should happen]
- **Scorecard:** Think Before Writing [Pass / Needs work], Simplicity [..], Goal-Driven [..]. (Surgical is how the edits below are made, not scored.)

**Findings** (most important first, max 6):
1. [Principle] Quote the exact line. What's wrong in one sentence. Suggested minimal fix (replacement line, or "cut").

**Leave alone:** 1-3 lines that are working and why, so they know what not to touch.

**Questions for the author** (only if something is genuinely ambiguous).

Then, if they ask for it or there are 3+ findings, offer the **edited post** with only the suggested changes applied, so they can see the diff in context. Every changed line must come from a finding above; don't add new sentences, facts or ideas no finding called for, and use `[placeholders]` for details only the author has. Never return a full rewrite unprompted.

For multiple posts, finish with **Patterns across posts**: 2-4 recurring issues (e.g. "ends with a generic question in 4 of 5", "two ideas per post").

## Tone of the review

Direct and specific, like a senior editor who respects the writer. Quote lines rather than describing them. No praise padding, no softening a real problem. If a post is already good, say so in one line and keep findings to what actually matters.