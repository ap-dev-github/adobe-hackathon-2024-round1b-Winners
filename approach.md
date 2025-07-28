# Approach: Persona-Keyword Mapping

## 🧩 Problem Statement
We were required to build a system that maps a **given persona** (like `student`, `researcher`, etc.) and a **job type** (like `summary`, `analysis`, etc.) to relevant sections of a document by extracting and ranking the **most relevant text**.

---

## 🧠 How It Works

### 1. PDF Parsing and Sectioning
- We use **`pdfplumber`** to extract characters and group them into lines and pages.
- Text lines are grouped using vertical position (for line formation) and font size (for heading detection).
- A rough document structure is inferred by:
  - Taking the **first few lines** as the document **title**
  - Extracting **headings** using text size (larger font size = higher heading level)

---

### 2. Keyword Mapping (Rule-Based)
- Each **persona** has a predefined list of relevant keywords.
- For example, a `student` may be interested in `"skills"`, `"projects"`, `"education"`, etc.

```
PERSONAS = {
    "student": ["skills", "project", "certifications", "internship"],
    "researcher": ["method", "experiment", "conclusion"],
    ...
}
```
