
# SEO Pulse – AI Marketing Intelligence Assistant

## Overview
SEO Pulse is a Python-based SEO auditing tool that crawls a website and analyzes its SEO performance. It provides an SEO score, identifies issues, and generates AI-powered recommendations to improve website visibility.

## Features
- Website crawling (up to 10 pages during testing)
- Title and meta description analysis
- H1 heading analysis
- Image alt text coverage
- Internal broken link checking
- Indexability analysis
- Canonical tag detection
- SEO score calculated using Python
- AI-powered SEO recommendations using Groq
- Streamlit user interface
- FastAPI backend
- Automated testing using Pytest

## Technologies Used
- Python
- FastAPI
- Streamlit
- BeautifulSoup
- Requests
- Pytest
- Groq API

## Project Structure
```text
seo-pluse/
├── app/
├── tests/
├── README.md
├── RESULTS.md
├── DECISIONS.md
├── AI_USAGE.md
└── requirements.txt
```

## Installation

1. Clone or download the project.
2. Open the project folder in VS Code.
3. Create and activate a virtual environment.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file and add your Groq API key:

```text
GROQ_API_KEY=your_api_key
```

## Running the Application

### Start the FastAPI backend

```bash
uvicorn app.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

### Start the Streamlit frontend

Open another terminal:

```bash
streamlit run app/ui.py
```

## Testing

Run:

```bash
pytest -v
```

Expected result: All 6 tests pass.

## SEO Scoring
The SEO score is calculated in Python using weighted SEO metrics. AI is used only to generate recommendations and does not calculate or modify the score.

## Security and Limitations
- Restricts crawling to the allowed domain.
- Limits the number of pages crawled.
- Uses request timeouts.
- Validates URLs and redirects.
- Checks robots.txt.
- Blocks detected localhost and private IP addresses.

This is an educational prototype and is not intended for unrestricted production crawling. DNS rebinding and other advanced network-security risks may still exist.

## Author
AI Marketing Intelligence Assignment
