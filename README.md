# 📧 Cold Mail Generator AI

An AI-powered Cold Email Generator that automatically creates personalized B2B cold emails from job postings.

## Features

* Extracts job information from job URLs
* Uses LLMs (Groq + LangChain) to understand job requirements
* Performs company research
* Matches portfolio projects with required skills
* Generates personalized cold emails
* Supports multiple email tones:

  * Professional
  * Technical
  * Executive
* Download generated emails

## Tech Stack

* Python
* Streamlit
* LangChain
* Groq LLM
* ChromaDB
* BeautifulSoup
* Pandas

## Project Workflow

1. User enters a job posting URL
2. Job details are scraped
3. Required skills are extracted
4. Portfolio projects are matched
5. Company research is performed
6. Personalized cold email is generated

## Screenshots

(Add screenshots here after deployment)

## Installation

```bash
pip install -r requirements.txt
streamlit run app/main.py
```

## Author

Anuhya
