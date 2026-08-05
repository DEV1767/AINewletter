# AI Research Newsletter Agent

An automated AI agent that **discovers, ranks, reads, summarizes, and delivers recent AI research papers as an email newsletter**.

Built with **LangGraph, RAG, Groq, Hugging Face Embeddings, FAISS, arXiv, and GitHub Actions**.

---

## The Problem

Keeping up with AI research is time-consuming. Hundreds of papers are published regularly, and manually searching, selecting, reading, and summarizing the useful ones takes hours.

## The Solution

This project automates the complete research workflow:

```text
Research Topic
      ↓
Search arXiv
      ↓
Rank Papers
      ↓
Select Top Papers
      ↓
Read PDFs
      ↓
RAG + Semantic Retrieval
      ↓
Generate Summaries
      ↓
Create HTML Newsletter
      ↓
Send via Email
```

The entire pipeline runs automatically on a schedule using **GitHub Actions**.

---

## Key Features

* Searches recent AI papers from **arXiv**
* Uses **LangGraph** to orchestrate the agent workflow
* Evaluates and ranks papers by relevance and usefulness
* Automatically selects the best papers
* Reads complete research PDFs
* Uses **RAG** to retrieve relevant sections instead of sending entire papers to the LLM
* Generates embeddings with `BAAI/bge-small-en-v1.5`
* Uses **FAISS** for semantic search
* Generates structured, grounded research summaries
* Creates a professional HTML newsletter
* Automatically sends the newsletter through Gmail
* Runs on a schedule using **GitHub Actions**

---

## Architecture

```text
START
  ↓
Research Agent
  ↓
arXiv Search
  ↓
Paper Evaluator
  ↓
Top Papers
  ↓
PDF Loader
  ↓
Chunking
  ↓
BGE Embeddings
  ↓
FAISS
  ↓
RAG Retrieval
  ↓
Paper Summarizer
  ↓
Newsletter Generator
  ↓
Email Sender
  ↓
END
```

---

## Tech Stack

| Technology     | Purpose                      |
| -------------- | ---------------------------- |
| Python         | Core application             |
| LangGraph      | Agent workflow orchestration |
| LangChain      | RAG pipeline                 |
| Groq           | LLM inference                |
| arXiv API      | Research paper discovery     |
| Hugging Face   | Local embeddings             |
| FAISS          | Vector search                |
| PyPDF          | PDF processing               |
| Gmail SMTP     | Email delivery               |
| GitHub Actions | Scheduling & automation      |

---

## Running Locally

```bash
git clone <YOUR_REPOSITORY_URL>
cd AINewletter

python -m venv myvenv
myvenv\Scripts\activate

pip install -r requirements.txt
python main.py
```

Create a `.env` file:

```env
GROQ_API_KEY_1=your_api_key
GROQ_API_KEY_2=your_api_key

APP_EMAIL=your_email@gmail.com
APP_EMAIL_PASSWORD=your_google_app_password
```

> Never commit API keys or `.env` files to GitHub.

---

## Automation

GitHub Actions automatically runs the pipeline on a schedule:

```text
GitHub Actions
      ↓
Install Dependencies
      ↓
Run Research Agent
      ↓
Generate Newsletter
      ↓
Send Email
```

Required GitHub Secrets:

```text
GROQ_API_KEY_1
GROQ_API_KEY_2
APP_EMAIL
APP_EMAIL_PASSWORD
```

---

## Future Improvements

* Prevent duplicate papers across newsletters
* Add configurable research topics
* Support multiple subscribers
* Add newsletter history and database storage
* Improve retry, logging, and failure handling
* Add a frontend dashboard

---

## What I Learned

This project helped me combine **LangGraph agents, tool calling, structured LLM outputs, RAG, embeddings, vector search, PDF processing, email automation, and GitHub Actions** into a complete end-to-end AI system.

---

## Author

**Shivam Chaudhary**

AI/ML Engineering Student | Backend Developer | Generative AI & Agentic AI
