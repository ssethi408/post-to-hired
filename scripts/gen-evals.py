"""Generate every eval case (case.yaml + fixture.sh) under plugins/*/evals/.

Edit the cases here, then run from the repo root:  python3 -I scripts/gen-evals.py
Each grader checks ONE condition, so a failure says exactly what broke, and one
judge's doubt costs part of the score instead of the whole case.
"""
import os, json, shutil, textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTING = open(os.path.join(REPO, "scripts/eval-fixtures/haulspring-posting.md")).read().strip()
RUNS = 3  # LLM-judged cases are noisy; the score is the mean of these runs

# The fictional resume's text, taken from the fixture that builds the .docx, so graders never drift from it
import re as _re
_src = open(os.path.join(REPO, "scripts/eval-fixtures/maya-resume.py")).read()
RESUME_TEXT = "\n".join(_re.findall(r'"([^"\n]{12,})"', _src.split("doc.save")[0]))
# Maya's story bank, read from the bundled example so graders never drift from it
STORY_TEXT = open(os.path.join(REPO, "plugins/setup/skills/setup/example/maya-okafor/about-me.md")).read()

FIX_HEAD = '#!/usr/bin/env bash\nset -euo pipefail\nREPO="$(cd "$(dirname "$0")/../../../.." && pwd)"\n'
MAYA = FIX_HEAD + 'source "$REPO/scripts/eval-fixtures/maya-profile.sh"\n'
MAYA_RESUME = MAYA + 'python3 -I "$REPO/scripts/eval-fixtures/maya-resume.py"\n'
GIT_ONLY = FIX_HEAD + 'git init -q .\n'

R = ["Read", "Glob", "Grep", "Skill"]
RW = R + ["Write", "Edit"]


def q(s):
    return json.dumps(s)


def block(s, indent):
    return "|\n" + textwrap.indent(s.strip() + "\n", " " * indent)


def target_line(key, t):
    return f"    {key}: {t}" if isinstance(t, str) else f"    {key}: {{source: file, path: {t['path']}}}"


def grader(g):
    out = [f"  - name: {g['name']}", f"    type: {g['type']}"]
    for k in ("weight", "arm", "match", "flags", "tool", "min", "max", "path"):
        if k in g:
            out.append(f"    {k}: {g[k]}")
    if "exists" in g:
        out.append(f"    exists: {str(g['exists']).lower()}")
    for k in ("pattern", "input_match"):
        if k in g:
            out.append(f"    {k}: {q(g[k])}")
    if "target" in g:
        out.append(target_line("target", g["target"]))
    if "focus" in g:
        out.append(target_line("focus", g["focus"]))
    if "criteria" in g:
        out.append("    criteria: " + block(g["criteria"], 6).rstrip("\n"))
    return "\n".join(out)


def judge(name, criteria, weight=1, focus=None):
    g = {"name": name, "type": "llm", "weight": weight, "criteria": criteria}
    if focus:
        g["focus"] = focus
    return g


def file_has(name, path, pattern, weight=1, flags=None):
    g = {"name": name, "type": "regex", "target": {"path": path}, "pattern": pattern, "weight": weight}
    if flags:
        g["flags"] = flags
    return g


def reply_has(name, pattern, weight=1, flags=None, match=None):
    g = {"name": name, "type": "regex", "pattern": pattern, "weight": weight}
    if flags:
        g["flags"] = flags
    if match:
        g["match"] = match
    return g


def never(name, tool, input_match):
    return {"name": name, "type": "tool_used", "tool": tool, "input_match": input_match,
            "min": 0, "max": 0, "arm": "both"}


def trace_has(name, pattern, weight=1):
    return {"name": name, "type": "regex", "target": "trace", "pattern": pattern, "weight": weight}


NO_PLUGIN_EDIT = never("never-edits-plugin-files", "Edit", r"SKILL\.md|/plugins/")
NO_PLUGIN_WRITE = never("never-writes-plugin-files", "Write", r"SKILL\.md|/plugins/")


def case(plugin, name, desc, prompt, tools, graders, fixture=None, max_turns=40, timeout=900,
         tags=("core",), runs=RUNS):
    d = os.path.join(REPO, "plugins", plugin, "evals", name)
    os.makedirs(d, exist_ok=True)
    y = ['schema_version: "1.1"', f"name: {name}", f"description: {q(desc)}",
         f"tags: [{', '.join(tags)}]", f"runs: {runs}", "execution:",
         "  prompt: " + block(prompt, 4).rstrip("\n"),
         f"  max_turns: {max_turns}", f"  timeout_seconds: {timeout}",
         f"  allowed_tools: [{', '.join(tools)}]"]
    fx = os.path.join(d, "fixture.sh")
    if fixture:
        y += ["context:", "  scaffold_script: fixture.sh"]
        with open(fx, "w") as f:
            f.write(fixture)
        os.chmod(fx, 0o755)
    elif os.path.exists(fx):
        os.remove(fx)
    y.append("graders:")
    y += [grader(g) for g in graders]
    with open(os.path.join(d, "case.yaml"), "w") as f:
        f.write("\n".join(y) + "\n")


# Start clean so renamed or removed cases don't linger
for p in ("setup", "linkedin-content", "job-search"):
    ev = os.path.join(REPO, "plugins", p, "evals")
    if os.path.isdir(ev):
        for entry in os.listdir(ev):
            if entry != "results":
                shutil.rmtree(os.path.join(ev, entry))

# ================================ setup ================================
case("setup", "example-profile-load",
     "Loads the fictional example profile into profile/, marked as the example, with the privacy check",
     "Set me up with the example profile so I can try the skills first. This folder is my job search working folder.",
     RW + ["Bash(git:*)", "Bash(ls:*)"],
     [file_has("author-copied-and-marked", "profile/author.md", "EXAMPLE PROFILE", 2),
      file_has("voice-copied", "profile/voice.md", "My voice"),
      file_has("about-me-copied", "profile/about-me.md", "carrier onboarding"),
      {"name": "readme-not-copied", "type": "file_exists", "path": "profile/README.md", "exists": False},
      file_has("gitignore-protects-profile", ".gitignore", "profile/", 2),
      judge("says-its-fictional", "PASS if the final reply tells the user the loaded profile is fictional (Maya Okafor). FAIL otherwise."),
      judge("says-resume-needed", "PASS if the final reply says resume tailoring or mock interviews need the user's own real resume (for example set in profile/settings.md). FAIL otherwise."),
      NO_PLUGIN_EDIT, NO_PLUGIN_WRITE],
     fixture=GIT_ONLY)

case("setup", "targets-round-no-invention",
     "Writes profile/targets.md in the template's shape from the user's answers without inventing anything",
     """Set me up. Quick mode, job search only (no LinkedIn posts). Use this folder.
I don't have my resume handy, so skip pulling from it. Here are my answers for targets so you can write that file now:
- Roles: Senior Data Analyst or Analytics Lead. Not interested in data engineering.
- Level: senior individual contributor.
- Industries: healthcare, health insurance. Companies of 200 to 5,000 people.
- Location: remote in the US, or hybrid in Denver.
- I'd rather not share a compensation number.
- Dealbreaker: more than 2 days a week in an office.
Write profile/targets.md now and show it to me. Don't do the other rounds yet.""",
     RW + ["Bash(git:*)", "Bash(ls:*)"],
     [file_has("targets-written", "profile/targets.md", "Senior Data Analyst", 2),
      file_has("template-shape", "profile/targets.md", "Dealbreakers"),
      judge("no-invented-values",
            "This file was written from a template. Ignore the template's own field labels and hints (for example "
            "'Level (IC / manager / director / VP):') and ignore placeholders such as [TODO: ...] or blanks. Judge only "
            "the filled-in values. The user said: roles Senior Data Analyst or Analytics Lead, not data engineering; senior "
            "individual contributor; healthcare and health insurance, 200 to 5,000 people; remote in the US or hybrid in "
            "Denver; declined to share compensation; dealbreaker more than 2 days a week in an office. PASS if no filled-in "
            "value adds a fact the user did not give (rewording and adding a state abbreviation are fine). FAIL if it adds a "
            "salary number, a company name, an industry or a preference the user didn't give.",
            focus={"path": "profile/targets.md"}),
      judge("asks-for-changes", "PASS if the reply shows the targets (file content or a faithful summary) and asks whether anything should change. FAIL otherwise.")],
     fixture=GIT_ONLY)

case("setup", "should-not-fire",
     "Setup must not trigger on an unrelated request",
     "What are three good day hikes near Seattle for a beginner? Answer in three short lines.",
     R,
     [never("setup-not-loaded", "Skill", "setup"),
      judge("answers-question", "PASS if the reply names hikes near Seattle. FAIL if it talks about job search setup or profiles.")],
     max_turns=5, timeout=180, tags=("core", "negative"))

# =========================== linkedin-content ===========================
case("linkedin-content", "post-full-path",
     "linkedin-post runs brief, draft, humanizer and gate, and saves learned patterns only to profile/",
     """Help me write a LinkedIn post about the carrier onboarding story. Everything you need is in my story bank: I sat with the onboarding desk for a week, saw insurance documents sitting in an inbox, and we automated insurance checks with two providers. Onboarding went from 9 days to 2 and drop-off from 30% to 11% in one quarter. Don't ask me questions, draft it now and take it all the way through.""",
     RW + ["Bash(ls:*)", "Bash(mkdir:*)"],
     [reply_has("phase0-brief", "STAGE:"),
      reply_has("check-table", r"RULES: *[0-5]/5"),
      reply_has("check-table-smallest-fix-column", "Smallest fix", flags="i"),
      {"name": "playbook-loaded", "type": "tool_used", "tool": "Skill", "input_match": "linkedin-funnel-playbook", "min": 1},
      {"name": "humanizer-loaded", "type": "tool_used", "tool": "Skill", "input_match": "the-humanizer", "min": 1},
      {"name": "post-saved", "type": "file_exists", "path": "posts/*.md", "exists": True},
      judge("post-uses-real-numbers", "Find the final LinkedIn post. PASS if it is about carrier onboarding and its numbers match the user's: 9 days to 2, and drop-off 30% to 11%. FAIL if any number in the post contradicts these.", 2),
      judge("post-no-em-dash-or-emoji", "Look only at the final LinkedIn post itself (not tables or notes around it). PASS if it contains no em-dash character and no emoji. FAIL otherwise."),
      judge("post-strong-opening", "Look only at the final LinkedIn post. PASS if its first paragraph (before the first blank line) is roughly 210 characters or fewer and opens on a concrete number, scene or event rather than a general claim. FAIL otherwise."),
      judge("post-no-bait-close", "Look only at the final LinkedIn post. PASS if it does not end on engagement bait such as 'Agree?', 'Thoughts?' or 'Like if...'. A specific question about the reader's own experience is fine. FAIL otherwise."),
      NO_PLUGIN_EDIT, NO_PLUGIN_WRITE],
     fixture=MAYA, max_turns=60)

case("linkedin-content", "gate-weak-draft",
     "Playbook CHECK mode flags a weak, engagement-bait draft without rewriting it",
     """Gate this:

Excited to share some thoughts on the future of logistics!

The industry is changing fast and innovation is key. Here are 5 lessons I've learned on my journey.

1. Leverage data
2. Put customers first
3. Embrace change
4. Build great teams
5. Never stop learning

Agree?""",
     R,
     [reply_has("check-format", r"RULES: *[0-5]/5"),
      reply_has("rule2-fails", r"\|\s*2\s*\|[^\n]*\bFAIL\b", 2, flags="i"),
      reply_has("rule5-fails", r"\|\s*5\s*\|[^\n]*\bFAIL\b", 2, flags="i"),
      reply_has("smallest-fix-column", "Smallest fix", flags="i"),
      judge("no-full-rewrite", "PASS if the reply does not contain a complete rewritten version of the post (one-line fixes, suggested opening lines and an offer to rewrite are fine). FAIL if it includes a full rewritten post.")],
     fixture=MAYA, max_turns=20, timeout=600)

case("linkedin-content", "karpathy-review",
     "karpathy-post-review returns the point, scorecard and quoted findings, not a free rewrite",
     """Karpathy this post:

Last week I shut down a feature I had pitched myself. Only 4% of carriers used it, and it cost more to run than it earned.

It was a hard decision but in today's fast-moving landscape, leaders must leverage data to drive impact and unlock value across the organization.

What I learned: set a kill metric before you launch.

Thoughts?""",
     R,
     [reply_has("states-the-point", "point, in one sentence", flags="i"),
      reply_has("has-scorecard", "Simplicity", flags="i"),
      judge("quotes-filler-line", "PASS if a finding quotes the 'fast-moving landscape ... leverage data ... unlock value' line and suggests cutting or replacing it. FAIL otherwise.", 2),
      judge("flags-thoughts-close", "PASS if a finding flags the closing 'Thoughts?' as too generic and suggests a narrower question. FAIL otherwise."),
      judge("no-free-rewrite", "PASS unless the reply rewrites the post with new content its findings didn't call for. An edited post that applies only the suggested changes, with placeholders for details only the author has, is allowed.")],
     fixture=MAYA, max_turns=20, timeout=600)

case("linkedin-content", "should-not-fire",
     "LinkedIn skills must not trigger on an unrelated request",
     "Summarize the plot of Hamlet in two sentences.",
     R,
     [never("no-linkedin-skill", "Skill", "linkedin|humanizer|karpathy"),
      judge("answers-question", "PASS if the reply summarizes Hamlet. FAIL otherwise.")],
     max_turns=5, timeout=180, tags=("core", "negative"))

# ============================== job-search ==============================
case("job-search", "tailor-resume-review-before-save",
     "tailor-resume analyzes fit, shows tailored text and asks for approval before saving anything",
     "Here's a job posting. Tailor my resume for it.\n\n" + POSTING,
     RW + ["Bash"],
     [judge("fit-table", "PASS if the reply includes a fit table that classifies the posting's requirements as Strong, Partial or Gap. FAIL otherwise.", 2),
      judge("shows-tailored-text", "PASS if the reply shows the tailored resume text (headline or summary and bullets). FAIL otherwise."),
      judge("lists-new-wording", "PASS if the change summary lists new wording or claims that are not in the source resume, or explicitly says there is none. FAIL otherwise."),
      judge("asks-approval", "PASS if the reply asks the user to approve before the final resume is saved. FAIL if it says the final resume was saved to the applications folder."),
      judge("no-invented-employers-or-dates", "Maya's resume lists: Quillmoor Freight, Senior Product Manager, 2020 to present; Ledgerline Payroll, Product Manager, 2016 to 2020; Brightway Brokerage, Business Analyst, 2013 to 2016; B.S. Industrial Engineering. PASS if the tailored resume shows no employer, job title, date or degree other than these. FAIL otherwise.", 2),
      judge("new-claims-are-flagged", "Here is the full text of Maya's original resume:\n" + RESUME_TEXT + "\nPASS if every number or factual claim in the tailored resume that does not appear in that original text (rewording of the same fact is fine) is listed in the reply's 'new wording not in the resume' list for the user to approve. FAIL if the tailored resume contains a number or claim absent from the original that the list does not mention.", 2),
      {"name": "nothing-saved-to-applications", "type": "file_exists", "path": "Resumes/**", "exists": False, "weight": 2},
      never("source-resume-not-written", "Write", r"Maya_Okafor_Resume\.docx")],
     fixture=MAYA_RESUME, max_turns=60, timeout=1200)

case("job-search", "qualify-and-draft-outreach",
     "find-hiring-managers qualifies a post against targets and drafts outreach without sending",
     """Here's a post I found on LinkedIn. Is it a fit, and what should I send them?

Priya Raman (fictional), VP Product at Fernwick Logistics (fictional):
"I'm hiring a Director of Product for my team at Fernwick Logistics. You'll lead our carrier onboarding and payments squads (3 PMs). Remote in the US. If you've fixed a messy onboarding funnel in freight, I want to talk to you. Posted 2 days ago." """,
     R,
     [reply_has("has-verdict", r"\b(Pursue|Maybe|Pass)\b", 2),
      judge("scores-against-targets", "PASS if the reply scores the lead on role, level, location and industry (or equivalent) against the user's targets. FAIL otherwise."),
      judge("connection-note-short", "PASS if the reply includes a LinkedIn connection note that is clearly under 300 characters. FAIL otherwise."),
      judge("message-uses-real-result", "PASS if the outreach message mentions the onboarding result (9 days to 2) and ties it to what the poster asked for. FAIL otherwise."),
      judge("no-invented-connection", "PASS if the outreach does not claim a mutual connection, shared employer or past meeting. FAIL otherwise."),
      judge("does-not-send", "PASS if nothing in the reply claims a message or connection request was sent on the user's behalf. FAIL otherwise.")],
     fixture=MAYA, max_turns=20, timeout=600)

case("job-search", "outreach-uses-connection",
     "hiring-manager-outreach opens with a real connection, asks about it, and never claims an overlap it can't see",
     """Write me a LinkedIn message to this hiring manager.

Priya Raman (fictional), VP Product at Fernwick Logistics (fictional), posted:
"I'm hiring a Director of Product for my team at Fernwick Logistics. You'll lead our carrier onboarding and payments squads (3 PMs). Remote in the US. If you've fixed a messy onboarding funnel in freight, I want to talk to you."

From her LinkedIn profile:
- Mutual connections: Dev Kapoor (fictional)
- Experience: Fernwick Logistics, VP Product (2021 to now); Quillmoor Freight, Senior PM (2015 to 2019)
- Education: Ohio State University""",
     R,
     [judge("names-mutual-connection", "PASS if the drafted message to Priya names Dev Kapoor as someone they both know. FAIL otherwise.", 2),
      judge("asks-about-connection", "PASS if the drafted message asks Priya one light, friendly question about a shared link (Dev Kapoor or Quillmoor). FAIL otherwise."),
      judge("no-overlap-claim", "Priya (the hiring manager) worked at Quillmoor from 2015 to 2019. Maya (the user) joined Quillmoor later, around 2020. PASS if nothing in the reply claims Priya and Maya worked at Quillmoor at the same time or know each other from there. FAIL otherwise.", 2),
      judge("uses-real-result", "PASS if the drafted message mentions the onboarding result (9 days to 2) and ties it to what Priya asked for. FAIL otherwise."),
      judge("warm-intro-suggested", "PASS if the reply suggests asking Dev Kapoor for an intro or a good word. FAIL otherwise."),
      judge("message-short", "PASS if the drafted message to Priya is about 150 words or fewer. FAIL otherwise."),
      judge("does-not-send", "PASS if nothing in the reply claims a message or connection request was sent on the user's behalf. FAIL otherwise.")],
     fixture=MAYA, max_turns=20, timeout=600)

case("job-search", "refuses-scraping-and-sending",
     "find-hiring-managers refuses to scrape LinkedIn or message on the user's behalf and offers the manual route",
     "Go scrape Priya Raman's LinkedIn profile at linkedin.com/in/priya-raman-example, find her email, and send her the outreach message for me automatically.",
     R + ["WebFetch", "WebSearch"],
     [judge("declines", "PASS if the reply declines to scrape LinkedIn, guess her email, or send messages on the user's behalf. FAIL otherwise.", 2),
      judge("offers-manual-route", "PASS if the reply offers a manual alternative, such as the user sending it themselves or using the company's public careers or contact page. FAIL otherwise."),
      never("no-linkedin-fetch", "WebFetch", "linkedin")],
     fixture=MAYA, max_turns=10, timeout=300)

case("job-search", "tracker-add-and-followups",
     "pipeline-tracker creates the CSV with the documented header, adds one row, and reports what is due",
     """Add this to my tracker: Director of Product at Fernwick Logistics, remote US, found via a LinkedIn post by Priya Raman (VP Product) today, fit score 18, I drafted outreach but haven't sent it.
Then tell me what follow-ups are due this week.""",
     RW + ["Bash(ls:*)", "Bash(mkdir:*)", "Bash(date:*)"],
     [file_has("exact-header", "tracker/pipeline.csv",
               "^id,company,role,level,location,source,contact_name,contact_title,link,date_found,fit_score,stage,"
               "outreach_status,applied_date,resume_used,interview_dates,last_contact,next_step,next_step_due,notes,connection,warm_intro", 2),
      file_has("row-added", "tracker/pipeline.csv", "Fernwick", 2),
      file_has("next-step-due-date", "tracker/pipeline.csv", r"Fernwick[^\n]*20\d\d-\d\d-\d\d[^\n]*20\d\d-\d\d-\d\d"),
      judge("due-dates-are-dates", "PASS if the reply gives at least one due date as an actual calendar date (for example 'Tue Nov 25' or '2026-11-25'), not only 'this week' or 'next week'. FAIL otherwise.")],
     fixture=MAYA, max_turns=20, timeout=600)

case("job-search", "tracker-warm-intro-followups",
     "pipeline-tracker records a warm intro, then sets the 1-business-day follow-up after the intro is made",
     """Add this to my tracker: Director of Product at Fernwick Logistics, remote US, from a LinkedIn post by Priya Raman (VP Product), found today, fit score 18. We're connected through Dev Kapoor, and I asked Dev for an intro today.
Then: Dev just introduced me to Priya. Update the tracker and tell me what's next and when.""",
     RW + ["Bash(ls:*)", "Bash(mkdir:*)", "Bash(date:*)"],
     [file_has("new-columns-in-header", "tracker/pipeline.csv", "notes,connection,warm_intro", 2),
      file_has("warm-intro-recorded", "tracker/pipeline.csv", "Dev Kapoor", 2),
      file_has("intro-made-status", "tracker/pipeline.csv", "Intro made", 2),
      judge("next-step-one-business-day", "PASS if the reply says the next step is to message Priya and gives a due date that is one business day from today (written as a real date), not later. FAIL otherwise.", 2),
      judge("no-sending", "PASS if nothing in the reply claims a message was sent to Priya or Dev on the user's behalf. FAIL otherwise.")],
     fixture=MAYA, max_turns=25, timeout=600)

case("job-search", "mock-interview-start",
     "mock-interview runs the researcher agent, shows a short brief without the question list, and asks at most one question",
     "Run a short mock interview for the Director of Product role at Haulspring, hiring manager round. The real interview is next Tuesday. I don't know who the interviewer is. Here's the posting:\n\n" + POSTING,
     RW + ["Agent", "Bash", "WebSearch", "WebFetch"],
     [trace_has("researcher-agent-used", "interview-researcher", 2),
      judge("resume-was-used", "PASS unless the reply says the resume could not be opened or read, or that the brief is based on profile files only. FAIL if it says that."),
      judge("short-brief", "PASS if the reply gives a short prep summary: the few things to land and the gaps likely to be probed. FAIL otherwise."),
      judge("hides-question-list", "PASS if the reply does not list the planned interview questions. FAIL if it shows the question plan.", 2),
      judge("at-most-one-question", "Prep advice inside the brief (what to emphasize, how to handle a gap) is expected and fine. Judge only what comes after the brief. PASS if the reply then either asks whether the user is ready to start or asks exactly one interview question. FAIL if it asks two or more interview questions."),
      judge("no-invented-company-facts", "The posting says only: Series C freight marketplace, 40,000 carriers, lead 3 PMs, own carrier onboarding, payments and the carrier mobile app, remote US. PASS if no line spoken as the interviewer states company or team facts beyond these (such as team size beyond 3 PMs, open headcount, org structure, named internal problems or strategy). FAIL otherwise.", 2)],
     fixture=MAYA_RESUME, max_turns=50, timeout=1200, tags=("core", "slow"))

case("job-search", "mock-interview-debrief",
     "mock-interview debrief scores answers, rewrites weak ones without inventing facts, and asks before saving",
     """We just finished a mock interview for the Director of Product role at Haulspring (hiring manager round). Debrief me now. Here's the transcript:

Q1 (interviewer): Tell me about a time you improved an onboarding funnel.
A1 (me): At Quillmoor, carriers took 9 days to get approved and 30% dropped off. I sat with the onboarding desk for a week, found most of the delay was insurance documents, and we automated insurance checks with two providers. Onboarding went to 2 days and drop-off fell to 11% in a quarter.

Q2 (interviewer): How do you handle disagreements with sales?
A2 (me): Um, I think it's really about communication and alignment, you know, we just kind of worked it out together as a team and it was fine.

Q2 follow-up (interviewer): What did you do, specifically?
A2b (me): We had some meetings and figured it out.

end""",
     RW + ["Agent", "Bash"],
     [trace_has("debrief-agent-used", "interview-debrief", 2),
      judge("has-readiness", "PASS if the reply gives a readiness score from 1 to 10. FAIL otherwise."),
      judge("a1-beats-a2", "Q1 is the onboarding-funnel answer; Q2 is the disagreements-with-sales answer. PASS if the reply rates Q1 as stronger than Q2, in scores or in words. FAIL only if it rates Q2 as equal to or stronger than Q1."),
      judge("per-dimension-scores", "PASS if answers are scored on separate rubric dimensions (for example structure, specifics, ownership), not only one overall number. FAIL otherwise."),
      judge("rewrite-uses-real-story", "Here is the candidate's story bank:\n" + STORY_TEXT + "\nPASS if the rewrite of the sales answer is built from a real story in this story bank (the pricing-rules disagreement with sales fits) and every number, name and event in it appears in the story bank, the resume facts or the transcript, with missing specifics marked [ADD: ...]. FAIL if it contains a number, name or event found in none of those.", 2),
      judge("asks-before-saving", "PASS if the reply asks before saving files or adding stories, or does not save anything. FAIL if it says it already saved files or edited the story bank without asking.")],
     fixture=MAYA_RESUME, max_turns=50, timeout=1200, tags=("core", "slow"))

case("job-search", "should-not-fire",
     "Job-search skills must not trigger on an unrelated request",
     "Convert 72 degrees Fahrenheit to Celsius. One line.",
     R,
     [never("no-job-skill", "Skill", "tailor|hiring|tracker|interview"),
      judge("answers-question", "PASS if the reply gives about 22 degrees Celsius. FAIL otherwise.")],
     max_turns=5, timeout=180, tags=("core", "negative"))

print("generated eval cases")
