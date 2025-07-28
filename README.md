# Adobe Hackathon Round 1B Submission 

##  Team: Winners  
###  Members:
- Ayush Pandey  
- Ayush Banerjee  

---

##  Goal  
To build a **Persona-Keyword Mapping** system that scans PDF documents and surfaces the most relevant sections for a given **persona** and **job role**. For example, a "student" looking for a "summary" of a document will receive relevant, ranked excerpts tailored to that context.

---

##  Tech Stack
- **Python 3.9 (slim)**
- **PDF Parsing:** `pdfplumber`
- No external NLP libraries were used. The system is fully **rule-based and deterministic**.

---

##  Docker Setup

### Dockerfile

```
FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/pdf_analyzer.py"]
```
## Build the Docker Image
```
docker build --no-cache --platform linux/amd64 -t adobe-1b .
```
## Run the Container
Run this command in PowerShell (Windows):
```
docker run --rm `
  -v "D:/adobe hackathon/adobe_hackathon_1b/input:/app/input" `
  -v "D:/adobe hackathon/adobe_hackathon_1b/output:/app/output" `
  -e PERSONA="student" `
  -e JOB="summary" `
  adobe-1b
```
## Output
The result will be stored in: output/output.json

Contains:

Matching sections

Page numbers

Section title

Importance rank

200-character preview of each section

## Dependencies
```
pdfplumber==0.10.3
```
Install via:
```
pip install -r requirements.txt
```
