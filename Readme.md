# AI Research Newsletter Agent

An automated AI research newsletter system built with **LangGraph, RAG, Groq, Hugging Face Embeddings, FAISS, and arXiv**.

The system searches for recent AI research papers, ranks the most useful ones, reads the top papers using a RAG pipeline, generates structured summaries, converts them into a professional HTML newsletter, and automatically sends the newsletter through email.

The entire workflow is automated using **GitHub Actions**.

---

## Why I Built This

Keeping up with AI research is difficult.

Every week, hundreds of new papers are published. Reading abstracts alone often isn't enough, while downloading and reading complete papers takes a lot of time.

Instead of manually doing:

```text
Search papers
     ↓
Open multiple papers
     ↓
Decide which are useful
     ↓
Read PDFs
     ↓
Understand the research
     ↓
Summarize everything
     ↓
Create a newsletter
```

I built an automated research agent that handles this workflow.

---

## How It Works

```text
                    Research Topic
                          │
                          ▼
                  ┌───────────────┐
                  │ Research Agent│
                  │   LangGraph   │
                  └───────┬───────┘
                          │
                          ▼
                     arXiv Search
                          │
                          ▼
                    Papers Found
                          │
                          ▼
                  ┌───────────────┐
                  │   Evaluator   │
                  │ Rank Research │
                  └───────┬───────┘
                          │
                          ▼
                    Top 3 Papers
                          │
                          ▼
                     PDF Loader
                          │
                          ▼
                       Chunker
                          │
                          ▼
                BGE Small Embeddings
                          │
                          ▼
                        FAISS
                          │
                          ▼
                  Semantic Retrieval
                          │
                          ▼
                  RAG Paper Summaries
                          │
                          ▼
                  Newsletter Generator
                          │
                          ▼
                   HTML Newsletter
                          │
                          ▼
                     Gmail SMTP
                          │
                          ▼
                       Inbox
```

---

## Features

- Searches recent research papers from arXiv
- Uses LangGraph for workflow orchestration
- Uses tool calling for research search
- Evaluates and ranks papers based on relevance and usefulness
- Automatically selects the highest-ranked papers
- Loads complete research paper PDFs
- Splits papers into smaller chunks
- Generates local embeddings using `BAAI/bge-small-en-v1.5`
- Creates FAISS vector stores
- Retrieves relevant research sections using semantic search
- Uses RAG to generate grounded paper summaries
- Generates a structured HTML research newsletter
- Sends the newsletter automatically through Gmail
- Runs automatically using GitHub Actions
- Supports separate API keys for different LLM tasks
- Caches the Hugging Face model in GitHub Actions

---

## RAG Pipeline

Instead of sending entire research papers to the LLM, the project uses **Retrieval-Augmented Generation (RAG)**.

```text
Research PDF
     ↓
Extract Pages
     ↓
Split into Chunks
     ↓
BGE Embeddings
     ↓
FAISS Vector Store
     ↓
Semantic Search
     ↓
Relevant Chunks
     ↓
LLM
     ↓
Grounded Summary
```

This reduces unnecessary LLM context usage and allows the summarizer to focus on the most relevant sections of each paper.

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| LangGraph | Agent workflow orchestration |
| LangChain | LLM and RAG components |
| Groq | LLM inference |
| arXiv API | Research paper discovery |
| Hugging Face | Local embedding model |
| BAAI/bge-small-en-v1.5 | Text embeddings |
| FAISS | Vector similarity search |
| PyPDF | PDF processing |
| Gmail SMTP | Newsletter delivery |
| GitHub Actions | Deployment and scheduling |

---

## Project Structure

```text
AINewletter/
│
├── .github/
│   └── workflows/
│       └── newsletter.yml
│
├── src/
│   ├── nodes/
│   │   ├── researcher.py
│   │   ├── evaluter.py
│   │   ├── pdf_loader.py
│   │   ├── chunker.py
│   │   ├── summarizer.py
│   │   ├── newsletter.py
│   │   └── email_sender.py
│   │
│   ├── tools/
│   │   ├── arxiv.py
│   │   └── email_sender.py
│   │
│   ├── rag/
│   │   ├── splitter.py
│   │   ├── vectorstore.py
│   │   └── retriver.py
│   │
│   ├── graph.py
│   └── state.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## LangGraph Workflow

The application uses a state-based LangGraph workflow.

```text
START
  │
  ▼
Researcher
  │
  ├── Tool Call ──► arXiv Search
  │                    │
  └────────────────────┘
  │
  ▼
Evaluator
  │
  ▼
PDF Loader
  │
  ▼
Chunker
  │
  ▼
RAG Summarizer
  │
  ▼
Newsletter Writer
  │
  ▼
Email Sender
  │
  ▼
END
```

The researcher can call the arXiv search tool, after which the retrieved papers continue through the rest of the pipeline.

---

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd AINewletter
```

### 2. Create a virtual environment

```bash
python -m venv myvenv
```

Activate it on Windows:

```bash
myvenv\Scripts\activate
```

On Linux/macOS:

```bash
source myvenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY_1=your_groq_api_key
GROQ_API_KEY_2=your_second_groq_api_key

APP_EMAIL=your_email@gmail.com
APP_EMAIL_PASSWORD=your_google_app_password
```

> Never commit `.env` or API credentials to GitHub.

---

## Running Locally

Run:

```bash
python main.py
```

The pipeline will:

1. Search for research papers
2. Rank the papers
3. Select the top papers
4. Load their PDFs
5. Build the RAG context
6. Generate summaries
7. Generate an HTML newsletter
8. Send the newsletter by email

---

## Automated Newsletter with GitHub Actions

The project uses GitHub Actions to run without requiring a continuously running server.

```text
GitHub Actions
      ↓
Temporary Linux Runner
      ↓
Install Python + Dependencies
      ↓
Restore Hugging Face Cache
      ↓
Run main.py
      ↓
Generate Newsletter
      ↓
Send Email
      ↓
Runner Stops
```

The workflow can also be manually triggered from:

```text
GitHub Repository
→ Actions
→ AI Research Newsletter
→ Run workflow
```

---

## GitHub Secrets

For automated execution, configure these repository secrets:

```text
GROQ_API_KEY_1
GROQ_API_KEY_2
APP_EMAIL
APP_EMAIL_PASSWORD
```

Go to:

```text
Repository
→ Settings
→ Secrets and variables
→ Actions
→ New repository secret
```

The credentials remain outside the source code.

---

## Weekly Scheduling

The GitHub Actions workflow is configured using cron scheduling.

Example:

```yaml
schedule:
  - cron: "30 2 * * 0"
```

This triggers the workflow every Sunday morning at approximately **8:00 AM IST**.

GitHub Actions schedules use UTC.

---

## Current Limitations

This is currently the first production version of the project.

Some planned improvements include:

- Prevent duplicate papers across newsletters
- Store processed paper IDs in a database
- Add better retry and failure handling
- Add configurable research topics
- Support multiple newsletter subscribers
- Add a frontend dashboard
- Add newsletter history
- Improve observability and logging
- Cache previously processed papers and embeddings

---

## Future Architecture

```text
                   User Preferences
                         │
                         ▼
                    Scheduler
                         │
                         ▼
                   Research Agent
                         │
                  ┌──────┴──────┐
                  ▼             ▼
               arXiv        Paper History
                  │           Database
                  └──────┬──────┘
                         ▼
                 Duplicate Filter
                         ▼
                     Ranking
                         ▼
                    Top Papers
                         ▼
                        RAG
                         ▼
                    Summaries
                         ▼
                    Newsletter
                         ▼
                  Email Subscribers
```

---

## What I Learned

Building this project helped me understand how different AI engineering concepts work together in a real pipeline:

- LangGraph state and node-based workflows
- LLM tool calling
- Structured LLM outputs
- Retrieval-Augmented Generation
- Local embedding models
- Vector databases
- Semantic retrieval
- PDF processing
- Multi-stage LLM pipelines
- HTML email generation
- Environment and secret management
- GitHub Actions automation
- Moving an AI workflow from local development to automated execution

---

## Disclaimer

The newsletter is generated using AI from research papers retrieved from arXiv. Generated summaries may occasionally miss context or contain inaccuracies. Refer to the original research papers for authoritative information.

---

## Author

**Shivam Chaudhary**

AI/ML Engineering Student | Backend Developer | Generative AI & Agentic AI

If you found this project useful, consider giving the repository a star.