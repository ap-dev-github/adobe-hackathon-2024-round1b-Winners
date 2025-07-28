import pdfplumber
import json
import os
from collections import defaultdict, Counter
from datetime import datetime


PERSONAS = {
    "researcher": ["method", "result", "data", "experiment", "conclusion", 
                  "hypothesis", "analysis", "findings", "benchmark"],
    "student": ["work experience", "skills", "project", "summary", "introduction",
               "certifications", "education", "internship"],
    "analyst": ["trend", "growth", "forecast", "quarterly", "revenue",
               "financial", "market share", "kpi", "metrics"]
}

def group_chars_to_lines(chars, y_tolerance=2):
    """Group characters into lines based on vertical position."""
    lines = defaultdict(list)
    for c in chars:
        key = round(c['top'] / y_tolerance) * y_tolerance
        lines[key].append(c)
    return lines

def join_chars_to_line_text(chars, x_tolerance=1.5):
    """Join characters into line text."""
    if not chars:
        return ""
    chars = sorted(chars, key=lambda c: c['x0'])
    text = chars[0]['text']
    for prev, curr in zip(chars, chars[1:]):
        if curr['x0'] - prev['x1'] > x_tolerance:
            text += ' '
        text += curr['text']
    return text.strip()

def extract_document(pdf_path, page_limit=10):
    """Extract structured content from a PDF."""
    with pdfplumber.open(pdf_path) as pdf:
        # Get title from first page
        first_page = pdf.pages[0]
        title_lines = []
        lines = group_chars_to_lines(first_page.chars)
        for _, chars in sorted(lines.items())[:2]:  # First 2 lines
            title_lines.append(join_chars_to_line_text(chars))
        title = "\n".join(title_lines).strip()

        # Process pages
        sections = []
        for page_num, page in enumerate(pdf.pages[:page_limit], 1):
            text = page.extract_text()
            if not text:
                continue

            # Extract headings (H1/H2)
            headings = []
            lines = group_chars_to_lines(page.chars)
            for _, line_chars in sorted(lines.items()):
                line_text = join_chars_to_line_text(line_chars)
                avg_size = sum(c["size"] for c in line_chars) / len(line_chars)
                if avg_size > 10:  # Heading threshold
                    headings.append(line_text)

            sections.append({
                "page": page_num,
                "headings": headings,
                "text": text
            })

    return {"title": title, "sections": sections}

def calculate_relevance(text, keywords):
    """Score text based on keyword matches."""
    text_lower = text.lower()
    return sum(
        1 for keyword in keywords 
        if keyword.lower() in text_lower
    )

def process_documents(input_dir, persona, job):
    """Process all PDFs and generate ranked output."""
    all_docs = []
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            doc = extract_document(os.path.join(input_dir, filename))
            all_docs.append(doc)

    # Rank sections
    keywords = PERSONAS.get(persona.lower(), [])
    ranked_sections = []
    for doc in all_docs:
        for section in doc["sections"]:
            score = calculate_relevance(section["text"], keywords)
            if score > 0:
                ranked_sections.append({
                    "document": doc["title"],
                    "page": section["page"],
                    "section_title": " | ".join(section["headings"][:2]) if section["headings"] else "Text",
                    "importance_rank": score,
                    "refined_text": section["text"][:200] + ("..." if len(section["text"]) > 200 else "")
                })

    # Sort by score (descending)
    ranked_sections.sort(key=lambda x: -x["importance_rank"])

    return {
        "metadata": {
            "input_documents": [doc["title"] for doc in all_docs],
            "persona": persona,
            "job": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "sections": ranked_sections
    }

if __name__ == "__main__":
    # Configuration (from environment variables)
    input_dir = os.getenv("INPUT_DIR", "/app/input")
    output_dir = os.getenv("OUTPUT_DIR", "/app/output")
    persona = os.getenv("PERSONA", "researcher")
    job = os.getenv("JOB", "analyze methods")

    # Process and save
    os.makedirs(output_dir, exist_ok=True)
    result = process_documents(input_dir, persona, job)
    
    with open(os.path.join(output_dir, "output.json"), 'w') as f:
        json.dump(result, f, indent=2)