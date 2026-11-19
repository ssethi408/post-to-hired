# Your profile

Every post-to-hired skill reads your `profile/` folder. It lives in the working folder you start Claude in, never inside the plugin.

The easiest way to fill it in is the `setup` skill: start Claude in your working folder and say "set me up". To do it by hand, copy the `.md` templates in this folder (not this README) into `profile/` and fill them in. For a finished example, see `../example/maya-okafor/`.

| File | Used by | What goes in it |
|---|---|---|
| `author.md` | linkedin-post, linkedin-funnel-playbook | Who you want engaging, what they get, goals, proof bank, jargon list, last 3 posts |
| `voice.md` | linkedin-post, karpathy-post-review, find-hiring-managers, mock-interview | How you write: tone, banned words, openings, closings, real samples |
| `about-me.md` | mock-interview, find-hiring-managers, linkedin-post | Your story bank: situation, what you did, result, lesson |
| `targets.md` | tailor-resume, find-hiring-managers, mock-interview | Roles, level, industries, location, comp, dealbreakers |
| `settings.md` | tailor-resume, pipeline-tracker, mock-interview | Where your master resume lives, where tailored PDFs go, where the tracker lives |
| `interview-rubric.md` | mock-interview (optional) | Extra scoring dimensions for your field |

The skills also create these as you use them, so your changes survive plugin updates:

| File | Created by | What's in it |
|---|---|---|
| `humanizer-patterns.md` | the-humanizer | New AI patterns it learned from your drafts |
| `calibration-posts.md` | linkedin-funnel-playbook | Your real posts with their rule results |
| `interviewer-styles/` | mock-interview | Interviewer styles you added |

If your working folder is a git repository, make sure `profile/` and `tracker/` are in its `.gitignore`. The setup skill checks this for you.
