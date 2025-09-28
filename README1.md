# 🧠 Agentic Deep Research Platform

A multi-agent AI system designed to perform comprehensive, deep research on any given topic. This project leverages LangGraph to orchestrate multiple specialized agents that work in parallel to gather, analyze, and synthesize information from various sources, presenting a final, coherent report to the user through a Streamlit interface.

**Current Date:** Saturday, 27 September 2025.

## ✨ Key Features

  * **Multi-Agent Architecture:** Utilizes a graph-based system where different agents have specialized roles.
  * **Parallel Execution:** Specialist agents for web, academic, news, and social media research run concurrently for maximum speed.
  * **Comprehensive Data Sources:** Gathers insights from:
      * General Web Search (Perplexity-style)
      * Academic Papers (Google Scholar & arXiv)
      * Latest News (News APIs)
      * Social Media Sentiment (Twitter/X & YouTube)
      * Financial Data (Stock APIs for relevant topics)
  * **Automated Synthesis:** A dedicated agent compiles all the gathered information into a single, structured report.
  * **Interactive UI:** A simple and clean user interface built with Streamlit.

## 🏛️ Architecture Overview

This system is built on a "divide and conquer" agentic architecture orchestrated by **LangGraph**.

1.  **Input:** A user provides a research topic via the Streamlit UI.
2.  **Orchestration:** An `Orchestrator` agent receives the topic, analyzes it, and creates a research plan, determining which specialist agents are needed.
3.  **Parallel Research:** The `Orchestrator` dispatches tasks to a team of specialist agents who work in parallel:
      * `WebResearcher`: Scours the web for general information.
      * `AcademicResearcher`: Queries arXiv and Google Scholar for papers.
      * `NewsAnalyzer`: Fetches recent articles from news APIs.
      * `SocialAnalyzer`: Analyzes sentiment and trends from social media.
      * `FinancialAnalyzer`: Pulls stock data if the topic is a public company.
4.  **Synthesis:** Once the specialist agents complete their tasks, a final `Synthesizer` agent gathers all their findings from the shared state. It then reads, analyzes, and synthesizes this diverse information into a single, comprehensive report.
5.  **Output:** The final report is displayed to the user in the Streamlit interface.

-----

## 📁 Project Structure

The project is organized into modular components to facilitate collaboration and maintainability. Each developer can own a specific agent or tool with minimal overlap.

```
/agentic_researcher
|
|-- app.py                    # Main Streamlit application entry point. Handles UI.
|
|-- /src
|   |-- /agents               # Core logic for each individual agent. Single responsibility.
|   |   |-- orchestrator.py     # Plans and delegates tasks. The "manager".
|   |   |-- web_researcher.py   # Agent for web searches.
|   |   |-- academic_researcher.py # Agent for Scholar/arXiv.
|   |   |-- social_analyzer.py    # Agent for YouTube/Twitter sentiment.
|   |   |-- news_analyzer.py      # Agent for News API.
|   |   |-- financial_analyzer.py # Agent for Stock API.
|   |   |-- synthesizer.py      # Compiles the final report from all other agent outputs.
|   |
|   |-- /tools                # Reusable functions that agents use to interact with external APIs.
|   |   |-- web_search_tools.py # Tools for browsing, scraping, etc.
|   |   |-- academic_tools.py   # Tools for arXiv and Scholar APIs.
|   |   |-- ... (and so on for each agent type)
|   |
|   |-- /graph                # The LangGraph definition. The "nervous system".
|   |   |-- state.py            # Defines the shared `ResearchState` object passed between agents.
|   |   |-- builder.py          # Wires all the agents together into a compiled graph.
|   |
|   |-- /prompts              # Stores agent prompts separately from code for easy editing.
|
|-- .env                      # Stores API keys and secrets (GITIGNORED).
|-- requirements.txt          # Project dependencies.
|-- README.md                 # This file.
```

-----

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1\. Clone the Repository

```bash
git clone <your-repository-url>
cd agentic_researcher
```

### 2\. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Set Up API Keys

API keys and other secrets are managed using a `.env` file.

1.  Make a copy of the example file:
    ```bash
    cp .env.example .env
    ```
2.  Open the `.env` file and add your secret keys. You will need keys for:
      * OpenAI (`OPENAI_API_KEY`)
      * Tavily AI for web search (`TAVILY_API_KEY`)
      * NewsAPI (`NEWS_API_KEY`)
      * Twitter/X Developer API, etc.

### 5\. Run the Application

Once the setup is complete, you can launch the Streamlit app from the **root directory**.

```bash
streamlit run app.py
```

Open your web browser to `http://localhost:8501` to use the application.

-----

## 🤝 How to Contribute

To ensure smooth collaboration during the hackathon, please follow this workflow:

1.  **Create a Branch:** Don't commit directly to `main`. Create a new branch for your feature.
    ```bash
    git checkout -b feature/my-cool-agent
    ```
2.  **Work on Your Module:** Develop your agent, tool, or UI component in your branch.
3.  **Open a Pull Request:** When your feature is ready, push your branch to the remote repository and open a Pull Request (PR) to merge into the `main` branch.
4.  **Code Review:** At least one other team member should review the PR before it is merged.

-----

## 🤖 For AI Agents & LLMs (Machine-Readable Scope)

**Objective:** This repository contains the source code for a multi-agent AI system that automates the process of in-depth research on a user-specified topic.

**Primary Input:** A single string variable `topic` provided by a human user.

**Primary Output:** A single string variable `final_report` which is a markdown-formatted synthesis of information gathered from multiple sources.

**Core Components:**

  * **Component: User Interface**
      * **Location:** `app.py`
      * **Function:** Renders a web interface using Streamlit, captures the `topic` input, and displays the `final_report` output.
  * **Component: State Management**
      * **Location:** `/src/graph/state.py`
      * **Function:** Defines the `ResearchState` TypedDict, a shared data structure that persists across agent executions.
  * **Component: Graph Orchestration**
      * **Location:** `/src/graph/builder.py`
      * **Function:** Uses the LangGraph library to define the nodes (agents) and edges (control flow) of the agentic system. It compiles the final executable graph.
  * **Component: Agent Logic**
      * **Location:** `/src/agents/`
      * **Function:** Each `.py` file in this directory represents a distinct agent. Each agent is a function that accepts the current `ResearchState` and returns a dictionary to update the state.
  * **Component: External Tools**
      * **Location:** `/src/tools/`
      * **Function:** These modules provide agents with access to external resources via API calls (e.g., web search, database queries). They are designed to be reusable and independent of agent logic.