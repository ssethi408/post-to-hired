---
name: "tailor-resume"
description: "Tailor the user's master resume to a job description, review it with them, then save a PDF in their applications folder under {Company}/{Role} - {YYYY-MM}. Use when the user shares a job posting and wants a resume for it."
---

# Tailor Resume to a Job

## Settings

Read these from `profile/settings.md` in the working folder you were started in (the `setup` skill writes it). Never search other folders or the rest of the computer for a profile. If the file or a value is missing, ask the user once and offer to save the answer there.

- RESUME_SOURCE: path to the user's master resume (.docx)
- APPLICATIONS_ROOT: folder where tailored resumes are saved
- OUTPUT_FILE_NAME: file name for every tailored PDF (the folder path is what distinguishes each application)
- RESUME_LENGTH_PAGES: target page count (default 2)

These live on the user's computer. If you can't read that folder from where you're running, ask the user for access or to share the file before starting.

## Step 1: Gather inputs
1. Get the job description. If the user gives a URL, fetch the page; if they paste text, use it. Extract: company name, exact role title, level, location, compensation if listed, and the 8 to 12 most important requirements and keywords.
2. Read RESUME_SOURCE (stage it from their computer, then extract text with pandoc). If the file is missing, ask the user where their current resume is instead of guessing.
3. Read `profile/targets.md` if it exists, for the level and focus the user is aiming for.
4. If company or role is unclear from the posting, ask before continuing.

## Step 2: Analyze fit
- Map each key requirement to evidence already in the resume. Classify each as Strong, Partial, or Gap. Do not invent experience to cover gaps.
- Flag level mismatch up front (e.g., an individual-contributor role vs. a senior leadership background, or the reverse) and tilt the tailoring accordingly: hands-on execution over org-building for IC roles, and the reverse for leadership roles.

## Step 3: Tailor the resume
Edit only what improves fit. Keep every fact true.
- Rewrite the headline and summary to match the role's focus. The headline must not claim a title or level the user hasn't held (no "Director-level" for someone whose highest title is Senior PM); describe the work instead ("Product leader, carrier onboarding and payments").
- Reorder bullets within each job so the most relevant come first.
- Reword bullets to use the posting's language where it honestly describes the same work.
- Surface relevant metrics (team size, scope, portfolio breadth) that are already in the resume.
- Trim, merge, or drop low-relevance bullets to keep the resume at RESUME_LENGTH_PAGES.
- Adjust the core competencies to lead with what the role asks for.
- Never add titles, employers, dates, degrees, numbers, or tools that are not in the source resume, unless the user supplies them in the conversation. Never use em-dashes (replace existing ones with commas or "to").

## Step 4: Review with the user (required, do not skip)
Show the user, in chat:
1. The full tailored resume text.
2. A short change summary: what moved, what was reworded, what was cut, and a **New wording not in RESUME_SOURCE** list: every phrase or claim that can't be traced word for word or in plain meaning to RESUME_SOURCE or `profile/about-me.md` (for example a new description of the company, a new collaborator, a new skill). Each item stays only if the user says yes. If there are none, say "none". Build this list mechanically before showing anything: go through the tailored resume line by line and check every number, duration, count, name and claim against RESUME_SOURCE's text. Anything you can't find there goes on the list, including details taken from `profile/about-me.md`.
3. The fit table from Step 2.
4. For each Gap or weak Partial, ask whether they have real experience not in the resume that would close it, and ask for specifics (counts, scope, named partners) that would make new bullets stronger. Only add what they confirm.
Apply their edits and show what changed. Once the text is close, build a preview PDF (Step 5.2) in a temporary folder outside APPLICATIONS_ROOT (for example the system temp directory) and send it so they see the real layout. Repeat until the user explicitly approves. Nothing goes into APPLICATIONS_ROOT, and RESUME_SOURCE is never touched, before approval.

## Step 5: Build and save
1. Build the folder path: APPLICATIONS_ROOT/{Company}/{Role} - {YYYY-MM}
   - Use the company's common name (e.g., "Acme", not "Acme, Inc.").
   - Use the exact role title from the posting and the current month (e.g., "2026-09").
   - Remove characters not allowed in folder names (/ \ : * ? " < > |).
   - If OUTPUT_FILE_NAME already exists there, ask before overwriting.
2. Build the PDF from a copy of RESUME_SOURCE so the original formatting is preserved:
   - If a docx skill is available, use its run-merging helper on the copy first (Word often splits one sentence across many runs, which makes in-place edits miss). Without one, merge adjacent runs in each paragraph that share the same formatting yourself with python-docx.
   - Edit paragraphs in place with python-docx: set run text, deepcopy an existing bullet paragraph for new bullets, remove paragraphs for cuts. Do not rebuild the document from scratch.
   - Convert to PDF with LibreOffice (`soffice --headless --convert-to pdf`). If python-docx or LibreOffice is missing, say which one and how to install it, and ask before installing anything.
3. Render the PDF pages to images and look at them: correct page count, no broken layout, no leftover old text, no em-dashes.
4. After approval, write the PDF to APPLICATIONS_ROOT/{Company}/{Role} - {YYYY-MM}/OUTPUT_FILE_NAME on their computer and tell the user the path in one line.
5. If they added new true facts during review, remind them in one line that RESUME_SOURCE doesn't have them yet and offer to update the master.

## Never
- Modify or overwrite RESUME_SOURCE without the user asking.
- Fabricate or inflate anything.
- Save to their computer before the user approves.
