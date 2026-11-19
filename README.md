# post-to-hired

Claude skills for a job search that runs on LinkedIn: write posts the right people reply to, tailor your resume to every role, and practice the interview before it happens.

Every skill holds the method. Your name, voice, stories and targets live in a `profile/` folder on your own computer that only you have. Install the plugins, let the setup skill build your profile, and the skills write like you and work toward the jobs you want.

You don't need to clone or fork this repo to use it. Fork it only if you want to change the skills themselves (see [Changing the skills](#changing-the-skills)).

## What's inside

**`setup` plugin**

| Skill | What it does |
|---|---|
| `setup` | Interviews you once and writes your profile: targets, settings, story bank, voice, LinkedIn author profile. Can load a fictional example profile so you can try everything first. Ends with a privacy check |

**`linkedin-content` plugin**

| Skill | What it does |
|---|---|
| `linkedin-post` | The default path for a post: picks the stage, reader and reply hook, drafts in your voice, humanizes it, then gates it against five rules |
| `linkedin-funnel-playbook` | Plans a week of posts, checks a draft against the five rules, or works out why a post flopped. Three stages: REACH, TEACH, CONVERSATION |
| `the-humanizer` | Finds AI-sounding patterns, scores the draft on four dimensions, and rewrites it in a human voice. Learns new patterns after every review |
| `karpathy-post-review` | Line-level review of a post using four principles: think first, keep it simple, make surgical edits, write toward a goal |

**`job-search` plugin**

| Skill / agent | What it does |
|---|---|
| `find-hiring-managers` | Qualifies hiring-manager posts you find on LinkedIn against your targets, researches the role, and drafts outreach in your voice. You do the searching and sending |
| `pipeline-tracker` | One row per opportunity, from lead to offer. Flags follow-ups that are due and gives a weekly summary |
| `tailor-resume` | Tailors your master resume to a job description, reviews every change with you, then saves a PDF per application |
| `mock-interview` | Runs a live mock interview for a specific role and stage, one question at a time, then debriefs every answer |
| `interview-researcher` (agent) | Builds the prep brief: what the role needs, gaps you'll be probed on, likely questions, your best story for each |
| `interview-debrief` (agent) | Scores the transcript, checks it against your resume, and rewrites your weakest answers without inventing facts |

Interviewer styles included: recruiter screen, hiring manager, skeptical bar-raiser, panel. Add your own in `profile/interviewer-styles/`.

## Quickstart

**1. Install** (in Claude Code):

```
/plugin marketplace add ssethi408/post-to-hired
/plugin install setup@post-to-hired
/plugin install linkedin-content@post-to-hired
/plugin install job-search@post-to-hired
```

Only want one half? Install `setup` plus just that plugin. If the skills don't show up right away, restart Claude Code.

**2. Make your profile.** Create a working folder for your job search (for example `~/job-search`), start Claude from it, and say *"set me up"*. The `setup` skill interviews you in short rounds, pulls what it can from your resume and a few things you've written, and writes your `profile/` folder there. Quick mode takes about 10 minutes, full mode about 30. You can stop after any round and pick it up later.

Want to try the skills before writing anything about yourself? Say *"set me up with the example profile"*. Setup loads a complete profile for Maya Okafor, a fictional product manager, and marks it as the example. Run setup again when you're ready, and it replaces Maya with you.

Prefer to fill it in by hand? The blank templates are in [`plugins/setup/skills/setup/templates/`](plugins/setup/skills/setup/templates/) and Maya's finished profile is in [`plugins/setup/skills/setup/example/maya-okafor/`](plugins/setup/skills/setup/example/maya-okafor/). Copy the templates into `profile/` and fill them in.

```
job-search/
└── profile/
    ├── author.md           who you want reading your posts, your proof bank
    ├── voice.md            how you write
    ├── about-me.md         your story bank
    ├── targets.md          what you're looking for
    ├── settings.md         where your resume lives, where PDFs go, where the tracker lives
    ├── interview-rubric.md optional
    ├── humanizer-patterns.md     created by the humanizer as it learns
    ├── calibration-posts.md      created by the playbook as you post
    └── interviewer-styles/       styles you add
```

Everything the skills learn about you is saved in `profile/`, never inside the plugins, so plugin updates never wipe it.

You don't have to fill everything in on day one. Each skill asks for what it's missing and offers to save your answer.

**3. Try it:**

- *"Help me write a LinkedIn post about the reorg I led last year."*
- *"Here's a job posting, tailor my resume for it."*
- *"Here's a post from a hiring manager. Is it a fit, and what should I send them?"*
- *"I have a hiring manager interview at Acme on Thursday. Run a mock interview."*
- *"What follow-ups are due this week?"*

## Make it yours

- **Voice:** `profile/voice.md` is where your writing style lives. Paste real samples. The more specific the file ("I never open with a question"), the better the output.
- **Rules:** each skill says which parts are meant to be changed. Funnel stages, gate rules, humanizer patterns and interview rubrics are all plain markdown.
- **Interviewer styles:** describe the interviewer you're expecting and mock-interview offers to save it to `profile/interviewer-styles/`. Or copy one of the [shipped styles](plugins/job-search/skills/mock-interview/interviewer-styles/) there and edit it.
- **The humanizer learns.** After every review it saves new AI patterns it caught to `profile/humanizer-patterns.md` and checks them in every review after that.

### Changing the skills

To change a skill's method rather than your own settings, fork this repo, edit the skill, and install from your fork with `/plugin marketplace add <your-username>/post-to-hired`. Your `profile/` folder works the same with your fork.

## Privacy

Your profile holds your resume, your stories and your targets. It never belongs in a public repo.

- It stays in your working folder on your own computer. Claude reads it during a session like any other file you work with, but no skill commits, publishes or sends it anywhere else.
- If your working folder is a git repository, setup checks that `profile/` and `tracker/` are in its `.gitignore`.
- This repo's own `.gitignore` blocks `profile/`, `tracker/`, `*.docx`, `*.pdf` and any call-notes file. If you fork it, check `git status` before every push.
- The proof bank in `author.md` marks every fact as shareable or not. Anything internal to an employer stays not shareable until you decide otherwise.

## A note on LinkedIn

These skills help you write, research and track. They don't scrape LinkedIn or automate your account, both of which LinkedIn's user agreement prohibits. You do the searching and the posting.

## Credits

The humanizer started from Aditya Vempaty's The Humanizer. The Karpathy review adapts Forrest Chang's andrej-karpathy-skills. Details in [CREDITS.md](CREDITS.md).

## License

MIT, see [LICENSE](LICENSE).
