import pdfplumber
from pathlib import Path

def extract_text_from_pdf(path: str) -> str:
    """
    Layout-aware extraction.
    Uses tolerances tuned for resumes.
    """
    pages_text = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:

            text = page.extract_text(
                x_tolerance=1,  # controls horizontal word joining
                y_tolerance=3,  # controls line grouping
                layout=True,  # VERY important for multi-column resumes
            )

            if text:
                pages_text.append(text)

    return "\n".join(pages_text)


def get_name():
    return "Vishwam Thakore"


def get_linkedin_text():
    path = Path("data") / "VishwamProfile.pdf"
    linkedin_text = extract_text_from_pdf(path=path)
    return linkedin_text


def get_summary():
    with open("data/summary.txt", "r", encoding="utf-8") as f:
        summary = f.read()
        return summary


def get_system_prompt():
    name = get_name()
    linkedin_text = get_linkedin_text()
    summary = get_summary()

    system_prompt = f"""
You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
Be polite and witty. \
Always use the tool record_unknown_question if you are unsure of the answer from the details provided. \
Do not make assumptions.""" 

    system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin_text}\n\n"
    system_prompt += f"With this context, please chat with the user, always staying in character as {name}."""
    return system_prompt

