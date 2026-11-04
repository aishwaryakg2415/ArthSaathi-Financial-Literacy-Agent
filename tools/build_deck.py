"""Fills the IBM SkillsBuild template with the ArthSaathi content.

Usage: python build_deck.py "<path to 2. Template.pptx>"
"""
import os
import sys
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor

ROOT = os.path.join(os.path.dirname(__file__), "..")
ASSETS = os.path.join(ROOT, "assets")
SCREENS = os.path.join(ASSETS, "screens")
OUT = os.path.join(ROOT, "ArthSaathi_Presentation.pptx")
RED = RGBColor(0xDA, 0x1E, 0x28)


def shape(slide, name):
    return next(s for s in slide.shapes if s.name == name)


def fill(sh, lines, size=16, font="Arial"):
    """lines: list of strings. '# ' = bold heading line, '**Label** rest' = bold label, '' = blank,
    '!' prefix = red text (things the student must replace)."""
    tf = sh.text_frame
    tf.word_wrap = True
    # the template uses shrink-on-overflow, which makes text tiny; turn it off
    bp = tf._txBody.bodyPr
    for child in list(bp):
        if child.tag.split('}')[1] in ("normAutofit", "spAutoFit", "noAutofit"):
            bp.remove(child)
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    first = tf.paragraphs[0]
    for r in list(first.runs):
        r._r.getparent().remove(r._r)
    for i, line in enumerate(lines):
        p = first if i == 0 else tf.add_paragraph()
        red = line.startswith("!")
        line = line.lstrip("!")
        parts = []
        if line.startswith("# "):
            parts = [(line[2:], True)]
        elif line.startswith("**") and "**" in line[2:]:
            label, rest = line[2:].split("**", 1)
            parts = [(label, True), (rest, False)]
        else:
            parts = [(line, False)]
        for text, bold in parts:
            if not text:
                continue
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.name = font
            r.font.bold = bold
            if red:
                r.font.color.rgb = RED
        p.space_after = Pt(2)


def replace_picture(slide, name_or_pic, img):
    """Put img in the old picture's box, keeping img's aspect ratio (centred)."""
    from PIL import Image
    pic = name_or_pic if not isinstance(name_or_pic, str) else shape(slide, name_or_pic)
    l, t, w, h = pic.left, pic.top, pic.width, pic.height
    pic._element.getparent().remove(pic._element)
    iw, ih = Image.open(img).size
    scale = min(w / iw, h / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    slide.shapes.add_picture(img, l + (w - nw) // 2, t + (h - nh) // 2, nw, nh)


def pictures(slide):
    return [s for s in slide.shapes if s.shape_type == 13]


def add_demo_slide(prs):
    """Adds a 'Demo' slide (Playground answers) right after the architecture slide."""
    from pptx.util import Emu
    s = prs.slides.add_slide(prs.slides[7].slide_layout)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    tb = s.shapes.add_textbox(Emu(537590), Emu(250000), Emu(11000000), Emu(500000))
    fill(tb, ["# Demo – ArthSaathi answering in the Langflow Playground"], size=24)
    w, h, top = Emu(3650000), Emu(5600000), Emu(950000)
    for i, name in enumerate(["q3_emi.png", "q5_otp.png", "q6_stock.png"]):
        replace_target = s.shapes.add_picture(os.path.join(SCREENS, name), Emu(350000 + i * 3850000), top, w, h)
        replace_picture(s, replace_target, os.path.join(SCREENS, name))
    cap = s.shapes.add_textbox(Emu(350000), Emu(6550000), Emu(11500000), Emu(300000))
    fill(cap, ["EMI via Calculator tool  ·  fraud emergency steps (1930)  ·  refuses stock tips (responsible AI)"], size=13)
    ids = prs.slides._sldIdLst
    el = ids[-1]
    ids.remove(el)
    ids.insert(8, el)


def add_bob_slide(prs):
    """Adds a 'Built with IBM Bob' slide right after the Demo slide."""
    from pptx.util import Emu
    s = prs.slides.add_slide(prs.slides[7].slide_layout)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    tb = s.shapes.add_textbox(Emu(537590), Emu(250000), Emu(11000000), Emu(500000))
    fill(tb, ["# Web app built with IBM Bob"], size=24)
    pic = s.shapes.add_picture(os.path.join(SCREENS, "bob_building_app.png"), Emu(350000), Emu(950000),
                               Emu(7300000), Emu(4600000))
    replace_picture(s, pic, os.path.join(SCREENS, "bob_building_app.png"))
    pic = s.shapes.add_picture(os.path.join(SCREENS, "web_scam.png"), Emu(7850000), Emu(950000),
                               Emu(4000000), Emu(4600000))
    replace_picture(s, pic, os.path.join(SCREENS, "web_scam.png"))
    cap = s.shapes.add_textbox(Emu(350000), Emu(5750000), Emu(11500000), Emu(900000))
    fill(cap, [
        "**Left: **IBM Bob generating the HTML/CSS/JS chat app from our prompt (BOB_PROMPTS.md).",
        "**Right: **the finished app – Scam Checker flags a fake SBI KYC SMS using the Langflow + Granite agent.",
    ], size=14)
    ids = prs.slides._sldIdLst
    el = ids[-1]
    ids.remove(el)
    ids.insert(9, el)


def main(template):
    prs = Presentation(template)
    S = prs.slides

    # 1 Title
    fill(shape(S[0], "Text Placeholder 2"),
         ["ArthSaathi – Agentic AI for Digital Financial Literacy, built with IBM Granite and Langflow"], size=22)

    # 2 Student details
    s = S[1]
    fill(shape(s, "TextBox 6"), ["**Project Title – **ArthSaathi: AI Agent for Digital Financial Literacy"], size=24)
    fill(shape(s, "TextBox 3"), ["**Domain of Project – **Finance / FinTech (Financial Inclusion)"], size=24)
    tb = shape(s, "TextBox 2")
    tb._element.getparent().remove(tb._element)
    table = next(x for x in s.shapes if x.has_table).table
    for c, txt in zip(table.rows[1].cells, ["Aishwarya KG", "", "aishwaryakg04xb@gmail.com", "+91 8217300447"]):
        fill(c, [txt], size=11)
    replace_picture(s, pictures(s)[0], os.path.join(ASSETS, "photo.jpg"))

    # 3 Problem statement (+ target users & pain points, required by guidelines)
    fill(shape(S[2], "TextBox 1"), [
        "# Problem Statement No. 7 : AI Agent for Digital Financial Literacy",
        "India now makes billions of UPI payments every month, but financial literacy has not kept pace. "
        "Millions of first-time digital users do not understand UPI safety, loan interest, budgeting or the "
        "government schemes meant for them – and online financial fraud is rising fast.",
        "",
        "# Why it matters",
        "**Scams: **fake KYC links, \"enter PIN to receive\" QR codes, digital-arrest calls and illegal loan apps drain savings – mostly from people who don't know the warning signs.",
        "**Debt traps: **people take loans without understanding flat vs. reducing rates, APR or EMI burden.",
        "**Exclusion: **useful schemes (PMJDY, PMSBY, APY) go unused because information is scattered and in English.",
        "",
        "# Target users & pain points",
        "Students, senior citizens, homemakers, small vendors and rural families. They have no one to ask, "
        "official info is scattered across RBI/NPCI/government sites, it is full of jargon, and they fear "
        "asking \"silly\" questions at a bank.",
        "**Why current solutions fail: **static FAQ pages and awareness videos can't answer *my* question, "
        "can't check *my* suspicious message and can't calculate *my* EMI; generic chatbots aren't grounded "
        "in trusted sources and may hallucinate numbers.",
    ], size=18)

    # 4 Proposed solution
    fill(shape(S[3], "TextBox 1"), [
        "# Proposed Solution: ArthSaathi – a RAG-powered financial literacy agent",
        "ArthSaathi (\"money companion\") is an agentic AI assistant built in Langflow and powered by IBM Granite "
        "models on IBM watsonx.ai. Users ask questions in their own language and get simple, step-by-step, "
        "source-grounded answers.",
        "",
        "**1. Trusted knowledge base (RAG): **RBI, NPCI, I4C and government-scheme material is parsed with Docling, "
        "chunked, embedded with a Granite embedding model on watsonx.ai and stored in Langflow's vector store.",
        "**2. Agent with tools: **a Granite-powered Langflow Agent decides when to search the knowledge base and "
        "when to use the Calculator (EMI, interest, budget split).",
        "**3. Scam Checker: **paste any suspicious SMS/WhatsApp – the agent lists red flags, gives a verdict and next steps.",
        "**4. Emergency mode: **if a user was just cheated, it first directs them to 1930 / cybercrime.gov.in and the bank.",
        "**5. Multilingual: **replies in the user's language (English, Hindi, Kannada, Tamil, …).",
        "**6. Simple web app (built with IBM Bob): **large-text chat, quick-question chips, PIN/OTP blocker, 1930 banner.",
        "",
        "**Value: **24x7 trusted guidance, fewer fraud losses, better loan decisions and higher scheme uptake – "
        "at near-zero cost per user, ready to scale through banks, colleges and CSCs.",
    ], size=16)

    # 5 Technology used
    fill(shape(S[4], "TextBox 2"), [
        "**Langflow – **visual design and orchestration of the RAG pipeline and the tool-using agent.",
        "",
        "**IBM Granite models – **ibm/granite-4-h-small (reasoning, multilingual answers, tool calling) and "
        "Granite embedding model for semantic search.",
        "",
        "**IBM watsonx.ai (IBM Cloud Lite) – **hosts and serves the Granite models and embeddings through a secure "
        "project with API-key access and governance.",
        "",
        "**Docling – **converts trusted PDFs / web pages / documents into clean structured text for the knowledge base.",
        "",
        "**RAG (Retrieval-Augmented Generation) – **retrieves trusted content first, then generates, so answers are "
        "grounded and cite their source.",
        "",
        "**IBM Bob – **AI coding assistant used to build and review the web chat front-end.",
    ], size=17)

    # 6 Langflow components
    fill(shape(S[5], "TextBox 1"), [
        "",
        "**1) Chat Input – **receives the user's question or pasted suspicious message.",
        "**2) Agent (IBM watsonx.ai) – **plans and calls tools; instructions enforce safety rules.",
        "**3) IBM Granite model – **ibm/granite-4-h-small → fast, multilingual, supports tool calling.",
        "**4) Chat Output – **returns the step-by-step answer with source and safety tip.",
        "**5) Docling + Export DoclingDocument – **parse knowledge documents.",
        "**6) Split Text – **800-character chunks, 150 overlap.",
        "**7) IBM watsonx.ai Embeddings – **Granite embedding model.",
        "**8) Local DB (vector store) – **ingest mode + retrieve mode as the knowledge_base tool.",
        "**9) Calculator – **tool for EMI, interest and budget maths.",
    ], size=18)

    # 7 Langflow workflow screenshot
    replace_picture(S[6], pictures(S[6])[0], os.path.join(SCREENS, "flow_canvas.png"))

    # 8 Architecture
    replace_picture(S[7], pictures(S[7])[0], os.path.join(ASSETS, "architecture.png"))

    # 9 Role of agentic AI
    fill(shape(S[8], "TextBox 2"), [
        "# Role of Agentic AI in ArthSaathi",
        "ArthSaathi is not a fixed FAQ bot. The Granite-powered agent reasons about each request and decides "
        "its own steps:",
        "**Understands & adapts – **detects intent and language, replies in the same language.",
        "**Safety first – **spots PIN/OTP sharing or fresh fraud and switches to emergency guidance.",
        "**Chooses tools – **searches the trusted knowledge base for facts; uses the Calculator for EMI, interest and budgets.",
        "**Acts as a scam checker – **analyses a pasted message, lists red flags and gives a verdict.",
        "**Grounded & honest – **answers only from retrieved sources, cites them and says \"not sure\" when the data isn't there.",
        "**Conversational memory – **keeps the session context so follow-up questions work naturally.",
        "Result: a proactive, personalised and trustworthy digital money companion.",
    ], size=16)
    replace_picture(S[8], pictures(S[8])[0], os.path.join(ASSETS, "agent_loop.png"))

    # 10 Token usage
    fill(shape(S[9], "TextBox 4"), ["41,419 tokens used across 11 test prompts (IBM Granite on watsonx.ai)"], size=16)
    shape(S[9], "TextBox 4").width = shape(S[9], "TextBox 4").width * 2
    fill(shape(S[9], "TextBox 13"), ["Prompt: EMI calculation (3.8K tokens)"], size=14)
    fill(shape(S[9], "TextBox 14"), ["Prompt: scam check (3.8K tokens)"], size=14)
    pics = pictures(S[9])
    replace_picture(S[9], pics[0], os.path.join(SCREENS, "q3_emi.png"))
    replace_picture(S[9], pics[1], os.path.join(SCREENS, "q2_scam.png"))
    for n in ["Google Shape;280;p18", "Google Shape;281;p18", "Google Shape;282;p18"]:
        fill(shape(S[9], n), [""], size=12)

    # 11 Novelty
    fill(shape(S[10], "TextBox 2"), [
        "ArthSaathi combines agentic reasoning, trusted RAG and safety-by-design into one simple companion for "
        "first-time digital finance users.",
        "",
        "**Scam Checker built in – **users paste a real message and get red flags + verdict + next steps, not generic tips.",
        "**Emergency-first fraud response – **guides to 1930 / cybercrime.gov.in within the RBI 3-day zero-liability window.",
        "**Grounded in Indian sources – **RBI, NPCI, I4C and scheme portals via Docling + Granite embeddings; no made-up numbers.",
        "**Agentic tool use – **calculates the user's own EMI, interest and 50/30/20 budget instead of just explaining formulas.",
        "**Multilingual & inclusive – **replies in the user's language with very simple words; large-text UI for elders.",
        "**Privacy by design – **front-end blocks PIN/OTP/card numbers before they are ever sent; no user data stored.",
        "**Low-cost & scalable – **runs on IBM Cloud Lite + Langflow; can be embedded by banks, colleges, NGOs and CSCs.",
    ], size=16)

    # 12 GitHub
    fill(shape(S[11], "Google Shape;279;p18"), [
        "https://github.com/aishwaryakg2415/ArthSaathi-Financial-Literacy-Agent",
        "",
        "Repository contains:",
        "1) app.json – exported Langflow flow (without API keys)",
        "2) Problem_Statement_7.pdf",
        "3) ArthSaathi_Presentation.pptx",
        "4) knowledge/ – RAG source documents",
        "5) web/ – chat front-end built with IBM Bob",
        "6) README.md – setup and run steps",
    ], size=16)
    for n in ["Google Shape;280;p18", "Google Shape;281;p18", "Google Shape;282;p18"]:
        fill(shape(S[11], n), [""], size=12)

    # 13 Future scope
    fill(shape(S[12], "Google Shape;279;p18"), [
        "**1. Voice in local languages – **speak a question in Kannada/Hindi and hear the answer, for low-literacy users.",
        "**2. WhatsApp / IVR channel – **reach users on basic phones through the channels they already use.",
        "**3. watsonx Orchestrate – **hand off to real actions such as raising a bank complaint or booking a branch visit.",
        "**4. Live updates – **scheduled Docling ingestion of new RBI circulars and scam alerts.",
        "**5. Learning journeys – **short quizzes and badges that track a user's financial-literacy progress.",
        "**6. Partnerships – **deploy with banks, colleges, SHGs and Common Service Centres.",
    ], size=16)
    for n in ["Google Shape;280;p18", "Google Shape;281;p18", "Google Shape;282;p18"]:
        fill(shape(S[12], n), [""], size=12)

    # 14, 15 Certificates
    replace_picture(S[13], pictures(S[13])[0], os.path.join(ASSETS, "credly_certificate.png"))
    replace_picture(S[14], pictures(S[14])[0], os.path.join(ASSETS, "bob_certificate.png"))

    add_demo_slide(prs)
    add_bob_slide(prs)
    prs.save(OUT)
    print("saved", os.path.abspath(OUT))


if __name__ == "__main__":
    main(sys.argv[1])
