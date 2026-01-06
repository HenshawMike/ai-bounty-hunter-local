# Local AI Bug Hunter 🔒

**A fully local, privacy-first AI-powered vulnerability scanner**

Local AI Bug Hunter is a hybrid **agentic RAG security analysis system** that combines deterministic static analysis with grounded LLM reasoning to produce **accurate, explainable, and actionable vulnerability reports** — all while keeping your code **100% offline**.

---

## ✨ Key Highlights

- 🔐 **Fully Local & Private** — No cloud calls. No data leakage.
- 🧠 **Hybrid Intelligence** — Semgrep for rule-based scanning + LLM reasoning for context and fixes.
- 📚 **Grounded AI (RAG)** — Uses a local knowledge base (OWASP, CWE, CVE patterns) to reduce hallucinations.
- 🔁 **Agentic Workflow** — LangGraph-powered stateful agent with conditional refinement loops.
- 🖥️ **Simple Web UI** — Streamlit interface for fast scans via paste or upload.
- 🧩 **Highly Extensible** — Add scanners, models, rules, or knowledge sources with ease.

---

## 🧠 Models Used (Local, January 2026)

| Purpose | Model |
|------|------|
| LLM Reasoning | `qwen2.5-coder:32b` |
| Embeddings | `nomic-embed-text:v2` |

---

## 🏗️ System Architecture

### High-Level Flow

```
User
 ↓
Streamlit UI (app.py)
 ↓
LangGraph Agent (graph/agent_graph.py)
 ├─ Semgrep Scanner
 ├─ RAG Retriever (Chroma)
 └─ LLM Reasoning Node
 ↓
Final Markdown Security Report
```

---

## 🔄 Data Flow Diagram

```mermaid
graph TD
    A[User Input<br>(Code paste / upload)] --> B[Streamlit UI<br>(app.py)]
    B --> C[LangGraph Agent<br>(agent_graph.py)]

    C --> D[Semgrep Scanner<br>(Deterministic)]
    C --> E[RAG Retriever<br>(Chroma DB)]

    D --> F[Findings JSON]
    E --> G[Retrieved Knowledge Context]

    F --> H[LLM Analysis Node<br>(Qwen2.5-Coder)]
    G --> H

    H --> I[Final Report<br>(Markdown)]
    I --> B
```

---

## 🧩 Core Components

| Component | Technology | Role |
|--------|-----------|------|
| UI | Streamlit | Code input & report display |
| Agent Orchestration | LangGraph | Stateful, conditional workflow |
| Static Analysis | Semgrep | Fast, reliable vulnerability detection |
| Retrieval (RAG) | Chroma + Ollama | Grounding LLM outputs |
| LLM | Qwen2.5-Coder | Deep reasoning & remediation |
| Knowledge Base | Local docs | OWASP, CWE, CVE references |

---

## 📦 Quick Start

### Prerequisites

- Python **3.10+**
- **Ollama** installed and running
- Semgrep installed

---

### 1️⃣ Pull Required Models

```bash
ollama pull qwen2.5-coder:32b
ollama pull nomic-embed-text:v2
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Build the RAG Knowledge Base

Place reference documents in:

```
rag/data/sources/
```

Then ingest:

```bash
python rag/ingestor.py
```

---

### 4️⃣ Run the App

```bash
streamlit run app.py
```

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

- Model tags
- Retrieval parameters
- Agent loop limits

---

## 🤝 Contributing

Contributions are welcome via issues and pull requests.

---

## ⚠️ Ethical Use Disclaimer

This tool is intended **only for authorized testing**.

---

## 📄 License

MIT License

---

Built with ❤️ in January 2026