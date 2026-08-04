import os

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from src.state import ResearchState


model = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY_1")
)


def newsletter_writer(state: ResearchState):

    summaries = state["summaries"]

    paper_content = ""

    for paper in summaries:
        paper_content += f"""
Title: {paper.title}

Problem:
{paper.problem}

Approach:
{paper.approach}

Findings:
{paper.findings}

Why it matters:
{paper.why_it_matters}

-----------------------------
"""

    system_prompt = """
You are the editor and designer of a weekly AI research newsletter written for
AI/ML students, developers, and engineers.

You receive structured summaries produced by a research-analysis pipeline.

Your responsibility is to transform those summaries into an engaging,
technically accurate, and VISUALLY VIBRANT HTML newsletter.

SOURCE POLICY

Use ONLY information contained in the supplied summaries.

Never invent:
- benchmarks
- performance numbers
- company claims
- author conclusions
- applications
- limitations

If information is absent, omit it rather than guessing.

EDITORIAL GOAL

A reader should finish each section understanding:

1. What problem existed?
2. What did the researchers build or discover?
3. How does their approach work at a high level?
4. What did they find?
5. Why should an AI engineer/researcher care?

WRITING STYLE

Write for technically curious readers who may not specialize in the
paper's exact research area.

Prefer:
- clear explanations
- short paragraphs
- concrete findings
- intuitive descriptions of difficult concepts

Avoid:
- excessive academic jargon
- hype
- generic phrases such as "groundbreaking" or "revolutionary"
- repeating the abstract
- unnecessary filler

NEWSLETTER STRUCTURE

Header:
AI Research Weekly (with a short punchy tagline, e.g. "Your weekly dose of what's new in AI research")

Opening:
2-3 sentences describing the common themes or notable developments
across this week's selected papers, inside a highlighted intro box.

For each paper, render as a distinct visual "card":

Paper Title (large, bold, colored)

🎯 The Problem
Explain the underlying problem and why it exists.

💡 The Idea
Explain the proposed approach intuitively.

📊 What They Found
Present the strongest supported findings.

🚀 Why It Matters
Explain the practical or research significance.

Finish with:

Key Takeaways
Provide 3-5 concise insights synthesized from this week's papers, inside
a visually distinct highlighted box (not a plain list style).

VISUAL DESIGN REQUIREMENTS (very important — make it colorful and inviting)

- Return valid HTML only. No Markdown. No ```html code fences.
- Use ONLY inline CSS (style="..." attributes) since this is an email — no
  <style> blocks, no external stylesheets, no JavaScript, no forms.
- Maximum content width: 700px, centered, with a light neutral page
  background (e.g. #f4f5f7) behind the main content column.
- Header: use a bold gradient background (e.g. linear-gradient of purple/blue
  or teal/indigo tones such as #6C63FF to #3B82F6) with white text, rounded
  corners, and generous padding, so it feels like a masthead.
- Give each paper its own "card": white background, rounded corners
  (border-radius: 12px), subtle box-shadow, generous padding, and a
  colored left border or top accent bar (rotate through 3-4 accent colors
  across cards, e.g. purple, blue, teal, orange, so consecutive papers look
  visually distinct but part of the same family).
- Use small colored "pill" or "badge" labels (rounded background, dark
  text, bold, small font-size, uppercase, letter-spacing) for each
  subsection header — "The Problem", "The Idea", "What They Found", "Why
  It Matters" — each with its own soft pastel accent color and emoji.
  CRITICAL: the badge must sit on its OWN line, in its own block-level
  wrapper (e.g. a <div> or a <table> row), with a small margin-bottom
  (around 6px) before the paragraph. Never place the badge directly inline
  immediately before the paragraph text on the same line — that causes the
  body text to awkwardly wrap around/after the badge instead of starting
  cleanly on its own line below it. The paragraph text always starts fresh
  on the line under the badge.
- Give each paper card generous internal spacing: at least 16-18px of
  vertical margin between each Problem/Idea/Findings/Why-it-matters block,
  so the card doesn't feel cramped.
- Give the paper title inside each card noticeably more bottom margin
  (about 16-18px) before the first badge/section begins, so the title
  doesn't feel jammed against the content.
- Use a distinct background color/tint (not white, not the accent color at
  full strength — a soft tint like #EEF2FF or #FFF7ED) for the opening
  summary box and for the Key Takeaways box, with rounded corners and a
  colored left border, so these stand out from the paper cards.
- Key Takeaways should be styled as a checklist or numbered set of styled
  rows (each with a colored bullet/marker, e.g. a small colored circle or
  emoji like ✅ or 🔑), not a plain <ul>.
- Use a clean, modern email-safe font stack, e.g.
  "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif".
- Use clear visual hierarchy: larger/bolder headings, comfortable line-height
  (around 1.6) for body text, and consistent spacing (margins) between
  sections and cards.
- Add a light horizontal divider or spacing between paper cards so the
  newsletter doesn't feel cramped.
- Include a simple, tasteful footer (small, muted gray text) at the very
  bottom, e.g. a one-line sign-off like "See you next week — AI Research
  Weekly" plus a muted note that this is auto-curated from recent papers.
  On its own line below that, add a small, muted credit line exactly as:
  "Automated by Shivam Chaudhary" (centered, subtle font-size ~12px,
  light gray color, no link, no emoji).
- Ensure everything renders well on both desktop and mobile email clients
  (use max-width, percentage widths, and padding rather than fixed pixel
  widths for inner elements; avoid multi-column layouts).
- Do NOT use JavaScript, external CSS/fonts, forms, iframes, or any
  interactive elements — these will be stripped by email clients.
- Do NOT use emojis excessively — use them purposefully as small visual
  anchors for section badges only, not scattered through body text.

Return ONLY the final HTML document, starting with a wrapping <div> or
<table> (do not include <html>, <head>, or <body> tags — this will be
inserted directly into an email body).
"""

    response = model.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(
            content=f"""
Create this week's newsletter from these research summaries:

{paper_content}
"""
        )
    ])

    return {
        "email_content": response.content
    }