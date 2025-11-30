# PulseMedic-AI  
### **Your Personal AI-in-Healthcare News Assistant • Powered by Multi-Agent Intelligence + Local Llama 3.2**

Healthcare AI evolves daily — new models, clinical applications, hospital AI policies, FDA approvals, academic breakthroughs, ethical concerns, and digital health innovations appear across scattered blogs, newsletters, and journals.

Clinicians, researchers, and students don’t have time to check everywhere.

**PulseMedic-AI solves that.**

This multi-agent system automatically gathers AI-in-healthcare news from trusted sources, filters what truly matters, and summarizes everything into a clean daily digest using a **local Llama 3.2 model (via Ollama)** — completely free, private, and offline.

---
## Team

PulseMedic-AI is built by a two-member team:

- **Keerthana Srinivasan** — Developer & System Architect  
- **Varsha Srinivasan** — Agent Design & Research  

# Why PulseMedic-AI?

###  Before PulseMedic-AI
- Too many healthcare AI resources  
- No central place to track updates  
- Time wasted reading long articles  
- Notifications scattered across newsletters  

###  After PulseMedic-AI
- One dashboard  
- One button  
- One concise daily summary  
- Local AI-powered multi-agent reasoning  
- Complete privacy (no cloud, no PHI, no API keys)

---

#  Problem Statement

AI in healthcare is exploding, but staying updated is difficult because:

- News is fragmented across dozens of sources  
- Articles contain general digital-health content, not always AI  
- Professionals are busy — they need summaries, not endless reading  
- Many AI tools require API keys, subscriptions, or cloud dependence  

 Healthcare workers deserve a **simple, fast, private way** to stay updated on AI in medicine.

---

# Solution Overview

PulseMedic-AI is a **local, multi-agent AI system** that:

### 1. Fetches  
Collects articles from high-quality healthcare AI sources including:
- AIin.Healthcare  
- NEJM AI  
- AMA Health Care AI  
- STAT Health Tech  
- Digital Health Wire  
- Healthcare Dive  
- mHealthIntelligence  
- Axios AI+  
…and more.

### 2. Filters  
Removes irrelevant content via the Filter Agent to keep only **AI-in-medicine** topics.

###  3. Summarizes  
Uses **Llama 3.2 (Ollama)** to generate:
- 3–5 key bullet insights  
- Article-level summaries  
- Clean, readable phrasing  

###  4. Displays  
A clean Streamlit dashboard shows:
- The day’s key AI-in-healthcare developments  
- Full article links  
- Source details  

All in under **30 seconds**.

---

#  Multi-Agent Architecture

                  ┌────────────────────────────────────────┐
                  │    Curated Healthcare AI Sources       │
                  │ (RSS, newsletters, publications, blogs)│
                  └────────────────────────────────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │      1. Fetcher Agent      │
                     │ - Scrapes feeds & webpages │
                     │ - Normalizes article JSON  │
                     └────────────────────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │      2. Filter Agent       │
                     │ - Removes noise            │
                     │ - Keeps AI-in-medicine     │
                     │ - Ensures relevance        │
                     └────────────────────────────┘
                                    │
                                    ▼
                     ┌────────────────────────────┐
                     │    3. Summarizer Agent     │
                     │ - Llama 3.2 via Ollama     │
                     │ - Bullet-point summary     │
                     │ - Reasoned aggregation     │
                     └────────────────────────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────────────────┐
                    │                Streamlit UI               │
                    │  Dashboard • Daily Summary • Full Links   │
                    └──────────────────────────────────────────┘

---

#  Key Agent Concepts Demonstrated (Kaggle Requirements)

This project implements **more than 3** required agent concepts:

###  Multi-Agent Collaboration  
Three autonomous agents working in sequence with specialized roles.

###  Tool-Using Agents  
Fetcher Agent → uses RSS/HTTP tools  
Summarizer Agent → uses the **Ollama** LLM tool

### LLM Reasoning & Planning  
Summarizer Agent performs:
- Multi-step reasoning  
- Theme extraction  
- Medical-grade summarization  

### Clean Architecture & Orchestration  
Each agent is a modular component orchestrated by the main app.

### Secure, API-free, Local Execution  
Protects privacy — no cloud, no PHI, no API keys.

---

## Project Structure

```
PulseMedic-AI/
│
├── app/
│   └── main.py                 # Streamlit UI
│
├── agents/
│   ├── fetcher_agent.py        # Gets articles
│   ├── filter_agent.py         # Filters relevance
│   ├── summarizer_agent.py     # Llama-based summary
│   └── personalization_agent.py # Optional personalization
│
├── config/
│   └── settings.py             # Constants / settings
│
├── core/
│   ├── __init__.py
│   └── logging_utils.py        # Optional utilities
│
├── .env                        # Environment variables (ignored)
├── README.md
└── requirements.txt
```


---

## Setup Instructions

### 1. Install Python & Ollama

- Install Python 3.11+
- Install Ollama: https://ollama.com/download

Pull the model:

```bash
ollama pull llama3.2
```

### 2. Clone the Repository

```bash
git clone https://github.com/keerthanasrinivasan22/PulseMedic-AI.git
cd PulseMedic-AI
```

### 3. Create & Activate Virtual Environment

```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Dashboard

```bash
streamlit run app/main.py
```

App will open at:

```
http://localhost:8501
```


### Supported News Sources

PulseMedic-AI pulls from quality AI-in-medicine publishers:

AI in Healthcare (Innovate Healthcare)

NEJM AI

AMA Health Care AI

STAT Health Tech – AI in Healthcare

Modern Healthcare – Digital Health Intelligence

Healthcare Dive – IT Weekly

mHealthIntelligence

Digital Health Wire

Axios AI+

This ensures clinically grounded and medically relevant updates.

### Privacy & Security

- No API keys  
- No cloud model calls  
- No PHI processed  
- 100% local Llama 3.2 execution  
- HIPAA-respectful architecture  

---

### Future Enhancements

- Optional Gemini agent (bonus points)  
- Personalized summaries (clinician/student modes)  
- Cloud deployment via Cloud Run  
- Daily scheduled email digests  
- Topic trend analytics & visual insights  

