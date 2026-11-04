"""Draws the architecture diagram, agent loop and placeholder images used in the deck."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)

BLUE = "#0f62fe"
DARK = "#161616"
TEAL = "#007d79"
PURPLE = "#8a3ffc"
RED = "#da1e28"
GREY = "#f2f4f8"


def box(ax, x, y, w, h, title, sub="", color=BLUE, fill="white", tsize=13, ssize=10, ty=0.66, sy=0.30):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                linewidth=2, edgecolor=color, facecolor=fill))
    if sub:
        ax.text(x + w / 2, y + h * ty, title, ha="center", va="center", fontsize=tsize,
                fontweight="bold", color=color)
        ax.text(x + w / 2, y + h * sy, sub, ha="center", va="center", fontsize=ssize,
                color=DARK, linespacing=1.3)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=tsize,
                fontweight="bold", color=color)


def arrow(ax, x1, y1, x2, y2, label="", color=DARK, both=False):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="<|-|>" if both else "-|>",
                                 mutation_scale=16, linewidth=1.8, color=color))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.17, label, ha="center", fontsize=9,
                color=color, style="italic")


def architecture():
    fig, ax = plt.subplots(figsize=(15.6, 8.4), dpi=150)
    ax.set_xlim(0, 15.6)
    ax.set_ylim(0, 8.4)
    ax.axis("off")
    ax.text(7.8, 8.05, "ArthSaathi – Architecture (Langflow · IBM watsonx.ai · IBM Granite · Docling)",
            ha="center", fontsize=16, fontweight="bold", color=DARK)

    # IBM Cloud boundary
    ax.add_patch(FancyBboxPatch((3.6, 0.35), 11.75, 7.25, boxstyle="round,pad=0.02,rounding_size=0.2",
                                linewidth=1.5, edgecolor=BLUE, facecolor=GREY, linestyle="--"))
    ax.text(3.8, 7.35, "IBM Cloud (Lite) – watsonx.ai project", fontsize=11, color=BLUE, fontweight="bold")

    # User side
    box(ax, 0.2, 5.3, 3.0, 1.5, "User", "Students, elders, women,\nvendors, rural families\n(text, any language)",
        color=DARK)
    box(ax, 0.2, 2.9, 3.0, 1.6, "Web Chat App", "Built with IBM Bob\nquick chips · scam checker\nPIN/OTP blocker · 1930 banner",
        color=PURPLE)
    arrow(ax, 1.7, 5.3, 1.7, 4.5, both=True)

    # Langflow agent
    ax.add_patch(FancyBboxPatch((4.0, 3.7), 7.2, 3.35, boxstyle="round,pad=0.02,rounding_size=0.15",
                                linewidth=1.5, edgecolor=TEAL, facecolor="white"))
    ax.text(4.2, 6.75, "Langflow flow (query side)", fontsize=11, color=TEAL, fontweight="bold")
    box(ax, 4.25, 5.05, 1.6, 1.1, "Chat Input", color=TEAL, tsize=11)
    box(ax, 6.35, 4.65, 2.6, 1.9, "Agent", "IBM Granite instruct\n(watsonx.ai)\nplan → retrieve →\ncalculate → answer",
        color=BLUE, tsize=13, ssize=9.5)
    box(ax, 9.45, 5.05, 1.6, 1.1, "Chat Output", color=TEAL, tsize=11)
    box(ax, 4.25, 3.85, 2.2, 0.75, "Calculator tool", color=TEAL, tsize=10)
    box(ax, 8.6, 3.85, 2.45, 0.75, "knowledge_base tool", color=TEAL, tsize=10)
    arrow(ax, 5.85, 5.6, 6.35, 5.6)
    arrow(ax, 8.95, 5.6, 9.45, 5.6)
    arrow(ax, 5.35, 4.6, 6.6, 4.65, both=True)
    arrow(ax, 9.8, 4.6, 8.7, 4.65, both=True)

    # API link
    arrow(ax, 3.2, 4.0, 4.25, 5.35, color=PURPLE, both=True)
    ax.text(2.75, 4.95, "Langflow\nREST API", fontsize=9, color=PURPLE, style="italic", ha="center")

    # Guardrails
    box(ax, 11.55, 3.7, 3.6, 3.35, "Responsible-AI guardrails",
        "• Answers grounded in retrieved docs\n• Source shown with each answer\n• Never asks for PIN / OTP / CVV\n"
        "• No stock / fund tips – education only\n• Says \"not sure\" instead of guessing\n• Fraud → 1930 & cybercrime.gov.in first\n"
        "• Low temperature, no user data stored",
        color=RED, tsize=12, ssize=9.5, ty=0.86, sy=0.42)

    # Ingestion pipeline
    ax.text(4.2, 2.95, "RAG ingestion pipeline (run once / when sources update)", fontsize=11, color=TEAL,
            fontweight="bold")
    box(ax, 0.2, 0.55, 3.0, 1.8, "Trusted sources", "RBI · NPCI · I4C (1930)\nPMJDY / Jan Suraksha\nSEBI / NCFE material",
        color=DARK)
    box(ax, 4.0, 0.8, 2.0, 1.4, "Docling", "parse PDFs / web\npages / docs", color=PURPLE)
    box(ax, 6.5, 0.8, 1.9, 1.4, "Split Text", "800-char chunks\n150 overlap", color=TEAL)
    box(ax, 8.9, 0.8, 2.6, 1.4, "watsonx.ai\nEmbeddings", "Granite embedding\n(multilingual)", color=BLUE, tsize=11,
        ty=0.70, sy=0.24)
    box(ax, 12.0, 0.8, 3.1, 1.4, "Vector store", "Langflow Local DB\ncollection: arthsaathi_kb", color=TEAL)
    arrow(ax, 3.2, 1.5, 4.0, 1.5)
    arrow(ax, 6.0, 1.5, 6.5, 1.5)
    arrow(ax, 8.4, 1.5, 8.9, 1.5)
    arrow(ax, 11.5, 1.5, 12.0, 1.5)
    arrow(ax, 13.0, 2.2, 10.2, 3.85, "semantic search")

    fig.savefig(os.path.join(OUT, "architecture.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def agent_loop():
    fig, ax = plt.subplots(figsize=(6, 9), dpi=150)
    ax.set_xlim(0, 6)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.text(3, 8.55, "Agent reasoning loop", ha="center", fontsize=17, fontweight="bold", color=DARK)
    steps = [
        ("1. Understand", "intent + language", BLUE),
        ("2. Safety check", "PIN/OTP? fraud emergency?", RED),
        ("3. Plan", "which tool is needed?", PURPLE),
        ("4. Retrieve", "knowledge_base (RAG)", TEAL),
        ("5. Calculate", "EMI · interest · budget", TEAL),
        ("6. Answer", "simple steps + source + tip", BLUE),
    ]
    y = 7.3
    for i, (t, s, c) in enumerate(steps):
        box(ax, 0.6, y, 4.8, 0.95, t, s, color=c, tsize=13, ssize=10.5)
        if i < len(steps) - 1:
            arrow(ax, 3, y, 3, y - 0.3)
        y -= 1.25
    ax.add_patch(FancyArrowPatch((5.4, 1.0), (5.4, 7.7), connectionstyle="arc3,rad=0.35",
                                 arrowstyle="-|>", mutation_scale=16, linewidth=1.5, color=DARK,
                                 linestyle="--"))
    ax.text(5.95, 4.4, "follow-up\nquestion", fontsize=9.5, rotation=90, va="center", color=DARK)
    fig.savefig(os.path.join(OUT, "agent_loop.png"), bbox_inches="tight", facecolor="white")
    plt.close(fig)


def placeholder(name, text, w=11.5, h=5.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=100)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.15, 0.15), w - 0.3, h - 0.3, boxstyle="round,pad=0,rounding_size=0.2",
                                linewidth=3, edgecolor=RED, facecolor="#fff1f1", linestyle="--"))
    ax.text(w / 2, h / 2, text, ha="center", va="center", fontsize=22 if w > 6 else 15,
            color=RED, fontweight="bold", linespacing=1.5)
    fig.savefig(os.path.join(OUT, name), facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    architecture()
    agent_loop()
    placeholder("ph_flow.png", "REPLACE WITH SCREENSHOT\nof your Langflow flow canvas", 11.5, 5.5)
    placeholder("ph_tokens_before.png", "REPLACE:\nToken usage screenshot\nBEFORE prompt", 5.1, 2.9)
    placeholder("ph_tokens_after.png", "REPLACE:\nToken usage screenshot\nAFTER prompt", 5.7, 2.9)
    placeholder("ph_credly.png", "REPLACE WITH YOUR\nCredly certificate", 7.1, 5.3)
    placeholder("ph_bob.png", "REPLACE WITH YOUR\nIBM Bob certificate", 7.2, 4.7)
    placeholder("ph_photo.png", "Your\nphoto", 2.0, 2.1)
    print("images written to", os.path.abspath(OUT))
