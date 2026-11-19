"""Shared eval fixture: writes a fictional 1-page resume for Maya Okafor as a .docx
and points profile/settings.md at absolute paths inside the eval workspace.
Run from the eval workspace: python3 -I <repo>/scripts/eval-fixtures/maya-resume.py
"""
import os
from docx import Document

ws = os.getcwd()
doc = Document()
doc.add_heading("Maya Okafor", 0)
doc.add_paragraph("Senior Product Manager | Chicago, IL (remote) | maya.okafor@example.com")
doc.add_heading("Summary", 1)
doc.add_paragraph("Senior product manager with 11 years in B2B software, the last 6 in logistics. "
                  "Leads a team of 4 PMs owning carrier onboarding and payments.")
doc.add_heading("Experience", 1)
doc.add_paragraph("Quillmoor Freight, Senior Product Manager, 2020 to present")
for b in ["Cut carrier onboarding from 9 days to 2 by automating insurance checks; drop-off fell from 30% to 11%.",
          "Shut down same-day pay after 6 months at 4% adoption and moved the team to onboarding.",
          "Built three pricing rules that covered 4 of the 5 largest shippers in 7 weeks.",
          "Manage 4 product managers."]:
    doc.add_paragraph(b, style="List Bullet")
doc.add_paragraph("Ledgerline Payroll, Product Manager, 2016 to 2020")
doc.add_paragraph("Owned the employer onboarding flow for a payroll product.", style="List Bullet")
doc.add_paragraph("Brightway Brokerage, Business Analyst, 2013 to 2016")
doc.add_paragraph("Analyzed lane pricing and carrier performance for a freight brokerage.", style="List Bullet")
doc.add_heading("Education", 1)
doc.add_paragraph("B.S. Industrial Engineering")
doc.save(os.path.join(ws, "Maya_Okafor_Resume.docx"))

with open(os.path.join(ws, "profile", "settings.md"), "w") as f:
    f.write("# Settings\n\n"
            f"- RESUME_SOURCE: {ws}/Maya_Okafor_Resume.docx\n"
            f"- APPLICATIONS_ROOT: {ws}/Resumes\n"
            "- OUTPUT_FILE_NAME: Maya_Okafor_Resume.pdf\n"
            "- RESUME_LENGTH_PAGES: 1\n"
            "- TRACKER: tracker/pipeline.csv\n")
