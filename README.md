<div align="center">

# 🧠 Illuminous - Agentic Deep Research Platform

Advanced multi-agent research assistant orchestrating web, academic, news, social, financial, YouTube, and Perplexity-powered investigations into one cohesive report.

[![python](https://img.shields.io/badge/python-3.10+-blue.svg)](#prerequisites)
[![streamlit](https://img.shields.io/badge/streamlit-1.30+-red.svg)](https://streamlit.io/)
[![langgraph](https://img.shields.io/badge/langgraph-0.0.58-6441b5.svg)](https://langchain-ai.github.io/langgraph)
[![license](https://img.shields.io/badge/license-MIT-yellow.svg)](#license)

</div>

---

## 🗺️ Table of Contents
- [Overview](#overview)
- [Key Capabilities](#key-capabilities)
- [Architecture](#architecture)
- [Agent Workflow](#agent-workflow)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Keys](#api-keys)
- [Running the Application](#running-the-application)
- [How to Use](#how-to-use)
- [Project Structure](#project-structure)
- [Agent Details](#agent-details)
- [Cost Tracking](#cost-tracking)
- [API Integrations](#api-integrations)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

---

## 📦 Overview
Agentic Deep Research Platform is a Streamlit application backed by LangGraph that deploys a team of specialized agents. Each agent handles a research vertical (web, academic papers, news, social sentiment, finance, Perplexity deep search, and YouTube video summarization). Outputs are normalized, optionally embedded into LanceDB for semantic retrieval, and synthesized by an LLM into a polished report (Markdown + PDF).

---

## ✨ Key Capabilities
- ?? **Dynamic Agent Selection** – Toggle the research modules you need at run time.
- ?? **Parallel Retrieval** – Web, news, academic, social, financial, Perplexity, and YouTube agents fan out concurrently.
- ?? **LLM Orchestration** – GPT-4o powers synthesis, finance intent detection, and YouTube summarization.
- ?? **Perplexity Deep Search** – Real API client provides citations, usage stats, and cost estimates.
- ?? **YouTube Intelligence** – Captions retrieved via API (or Whisper fallback) then summarized.
- ?? **Comprehensive Reporting** – Markdown preview plus PDF export, archived state JSON, and optional vector-store indexing.

---

## 🏛️ Architecture

![System Architecture](docs/system-architecture.png)

---


## 🧩 Agent Workflow
1. **orchestrator** – Crafts research plan and determines which branches execute.
2. **Parallel agents** – Gather data from their respective domains.
3. **cleanup** – Clears previous archives/vector store to avoid cross-run contamination.
4. **data_archiver** – Saves entire research state as JSON.
5. **vector_store** – Chunks, embeds, and stores knowledge in LanceDB (optional).
6. **rag_retriever** – Performs semantic search on stored chunks for additional context.
7. **synthesizer** – Generates final markdown + PDF report.

---

## ✅ Features
- ? Domain-specific prompt templates for synthesizer, Perplexity, and YouTube summarization.
- ? Token/cost tracking for every LLM invocation via centralized registry.
- ? Real-time workflow dashboard with detailed metrics.
- ? Archival system for reproducibility (data/json/...).
- ? Optional Whisper + FFmpeg fallback for YouTube captions, with detailed debug metadata.

---

## 📚 Technology Stack
- **Frontend**: Streamlit 1.30+
- **Workflow**: LangGraph 0.0.58
- **LLM Provider**: OpenRouter (GPT-4o, GPT-4o-mini, o1-mini, Gemini)
- **Vector Store**: LanceDB + Sentence Transformers (ll-MiniLM-L6-v2)
- **Transcription**: youtube-transcript-api, optional Whisper + yt-dlp + FFmpeg
- **Additional APIs**: Perplexity, Tavily, SearchAPI.io, NewsAPI, Twitter, Finnhub, Alpha Vantage, YouTube Data API
- **PDF Export**: ReportLab

---

## 📋 Prerequisites
- Python 3.10+
- pip / virtualenv
- FFmpeg (only if Whisper fallback enabled)
- Git (recommended)

---

## 🛠️ Installation
`ash
git clone https://github.com/<your-org>/agentic-deep-research.git
cd agentic-deep-research
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
`

---

## ⚙️ Configuration
1. Copy .env.example ? .env
2. Populate the necessary API keys (table below). Any blank key gracefully disables the related feature.
3. (Optional) Enable Whisper fallback:
   `env
   ENABLE_WHISPER_FALLBACK=1
   WHISPER_MODEL=base
   `
   Install openai-whisper, 	orch, yt-dlp, and ensure fmpeg is on PATH.

---

## 🔑 API Keys
| Service            | Env Variable(s)                             | Required | Notes |
|--------------------|----------------------------------------------|----------|-------|
| OpenRouter (LLMs)  | OPENROUTER_API_KEY                         | ?       | Primary LLM provider |
| HuggingFace        | HUGGINGFACE_API_KEY                        | ?       | Needed for some SentenceTransformer models |
| Perplexity         | PERPLEXITY_API_KEY                         | ?       | Enables Perplexity researcher |
| Tavily             | TAVILY_API_KEY                             | ?       | Web research enrichment |
| SearchAPI.io       | SEARCHAPI_API_KEY                          | ?       | Alternative SERP |
| NewsAPI            | NEWS_API_KEY                               | ?       | News aggregation |
| Twitter/X          | TWITTER_BEARER_TOKEN                       | ?       | Social sentiment |
| Finnhub            | FINNHUB_API_KEY                            | ?       | Financial news |
| Alpha Vantage      | ALPHAVANTAGE_API_KEY                       | ?       | Financial news |
| YouTube Data API   | YOUTUBE_API_KEY                            | ?       | Video search/details |
| Whisper Fallback   | ENABLE_WHISPER_FALLBACK, WHISPER_MODEL   | ?       | Requires local Whisper + FFmpeg |

> **Tip:** Once keys are in place, restart Streamlit so the environment is reloaded.

---

## ▶️ Running the Application
`ash
streamlit run app.py
`
Open [http://localhost:8501](http://localhost:8501) to interact with the dashboard.

---

## 🧭 How to Use
1. **Select Researchers** – Toggle the agents you want (Academic is preselected).
2. **Enter Topic** – Provide a concise research question.
3. **Start Research** – Click “Start Research” to launch the LangGraph workflow.
4. **Monitor Progress** – Watch agent-level metrics and logs in the left column.
5. **Review Results** – Read the final markdown, download the PDF, and inspect archives/vector data in the right column.

---

## 🗂️ Project Structure
```
agentic-deep-research/
├── app.py                  # Streamlit UI + workflow runner
├── requirements.txt        # Python dependencies
├── .env.example            # Sample environment variables
├── data/
│   ├── json/               # Archived research states
│   ├── vector_store/       # LanceDB database (optional)
│   └── youtube/            # Transcripts & metadata snapshots
├── docs/
│   └── system-architecture.png
├── src/
│   ├── agent/              # Agent implementations (web, news, social, etc.)
│   ├── graph/              # LangGraph builder + shared state
│   ├── tools/              # External API wrappers (Perplexity, Tavily, etc.)
│   ├── utils/              # LLM registry, config helpers, PDF exporter
│   └── prompts/            # Prompt templates for agents
├── README.md
└── README_Example.md
```

---

## 🤖 Agent Details
| Agent | Purpose |
|-------|---------|
| `orchestrator` | Drafts research plan, determines branching |
| `web_researcher` | DuckDuckGo / Tavily / SearchAPI SERP aggregation |
| `academic_researcher` | arXiv API + Google Scholar surface search |
| `news_analyzer` | NewsAPI or DuckDuckGo news fallback |
| `social_analyzer` | Twitter/X sentiment capture |
| `financial_analyzer` | Finance intent detection + Finnhub/Alpha Vantage |
| `perplexity_researcher` | Perplexity deep search with citations |
| `youtube_researcher` | Video discovery, transcription, summarization |
| `cleanup` | Clears archives and vector store between runs |
| `data_archiver` | Persists full state as JSON |
| `vector_store` | LanceDB embedding + chunk management |
| `rag_retriever` | Semantic retrieval over indexed knowledge |
| `synthesizer` | GPT-4o report generation (markdown + PDF) |

---

## 💰 Cost Tracking
- `invoke_llm` records tokens, cost, latency, and truncation flags per call.
- Streamlit footer summarizes session-level totals.
- Financial agent includes intent-check metrics even when finance research is skipped.

---

## 🌐 API Integrations
- Perplexity, Tavily, SearchAPI.io, DuckDuckGo (web search)
- arXiv, Google Scholar (academic)
- NewsAPI, DuckDuckGo (news)
- Twitter/X recent search (social)
- Finnhub, Alpha Vantage (financial)
- YouTube Data API + youtube-transcript-api (video)
- OpenRouter, Whisper (LLMs)

---

## 🔮 Troubleshooting
| Issue                                   | Resolution |
|----------------------------------------|------------|
| FFmpeg warnings / no YouTube transcripts | Install ffmpeg and ensure it’s on PATH; Whisper fallback depends on it |
| Perplexity error                        | Confirm PERPLEXITY_API_KEY and network connectivity |
| Empty social/financial sections         | Verify API keys and rate limits for Twitter/Finnhub/Alpha Vantage |
| LanceDB _distance warning             | Harmless deprecation note; future version will hide _distance automatically |
| Streamlit import crash                  | Check traceback—missing optional deps or env vars are the usual culprits |

---

## 🔮 Future Enhancements
- Conversational interface (chat) grounded in research results + vector store
- Visual analytics (charts, timelines, cost plots)
- Pluggable agent registry for user-defined data sources
- HTML/Notion export and scheduled digests
- Automated benchmarking and evaluation harness

---

## 📜 License
This project is released under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements
Huge thanks to the maintainers of LangChain, LangGraph, LanceDB, Sentence Transformers, Whisper, OpenRouter, and the data/API providers (Perplexity, Tavily, SearchAPI.io, NewsAPI, Twitter, Finnhub, Alpha Vantage, Google, YouTube) that enable this research experience.

---

## 📬 Contact
**Team Outskill Hackathon Group 4**  
- Shankar — lead2shankar@gmail.com  
- Sanjay — karwasanjay007@gmail.com  
- Imran — imranh0505@gmail.com  
- Shaibi — shaibis@gmail.com  
- Mrinal Pasari — mpasari@gmail.com  | https://www.linkedin.com/in/mrinalpasari/
- Anmol — anmol.mailme@gmail.com  

Let us know if you have feature ideas, encounter issues, or want to collaborate!




