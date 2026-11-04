"""Writes Problem_Statement_7.pdf (the problem statement file the GitHub repo must contain)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

OUT = os.path.join(os.path.dirname(__file__), "..", "Problem_Statement_7.pdf")

st = getSampleStyleSheet()
body = [
    Paragraph("IBM SkillsBuild for University Engagements – AICTE 2026", st["Title"]),
    Paragraph("Problem Statement No. 7 – AI Agent for Digital Financial Literacy", st["Heading2"]),
    Paragraph(
        "<b>The Challenge</b> – An AI Agent for Digital Financial Literacy, powered by RAG (Retrieval-Augmented "
        "Generation), helps users understand and navigate essential financial tools and practices.", st["BodyText"]),
    Paragraph(
        "• It retrieves reliable content on using UPI, avoiding online scams, understanding interest rates, "
        "budgeting, and personal finance management from government portals, banking websites, and educational "
        "platforms.<br/>"
        "• With multilingual support, users from diverse backgrounds can interact in their preferred language and "
        "ask questions like \"How do I send money via UPI?\" or \"What is a safe interest rate for a loan?\"<br/>"
        "• The agent ensures financial literacy is accessible, personalized, and culturally inclusive.<br/>"
        "• This AI-driven assistant empowers users with knowledge, protects them from fraud, and builds confidence "
        "in digital finance.", st["BodyText"]),
    Paragraph("<b>Technology</b> – Use of IBM Cloud Lite services / IBM Granite is mandatory.", st["BodyText"]),
    Spacer(1, 18),
    Paragraph("Our solution: ArthSaathi", st["Heading2"]),
    Paragraph(
        "ArthSaathi is a Langflow agent powered by IBM Granite on IBM watsonx.ai. Trusted RBI / NPCI / I4C / "
        "government-scheme material is parsed with Docling and embedded with a Granite embedding model for "
        "retrieval. The agent answers in the user's language, calculates EMIs and budgets with a calculator tool, "
        "checks suspicious messages for scam red flags, and directs fraud victims to the 1930 helpline. A simple "
        "web front-end was built with IBM Bob.", st["BodyText"]),
]
SimpleDocTemplate(OUT, pagesize=A4, leftMargin=50, rightMargin=50).build(body)
print("saved", os.path.abspath(OUT))
