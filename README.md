# 🇩🇪 German Tutor with Ollama, Streamlit, and ChromaDB

This project combines:
- A custom Ollama model for German tutoring (`german-teacher`)
- A Streamlit UI with slash commands and personalization
- Persistent memory via ChromaDB

## 🔧 Setup

### 1. Run ChromaDB via Docker

```bash
docker-compose up -d
```

### 2. Build Ollama model

```bash
ollama create german-teacher -f Modelfile
```

### 3. Install Python dependencies

```bash
pip install streamlit requests chromadb
```

### 4. Run the Streamlit app

```bash
streamlit run streamlit_app.py
```

---

## 💬 Slash Commands

- `/quiz` — Get a vocabulary or grammar quiz
- `/review` — Recall past vocabulary
- `/translate <text>` — Ask for translation
- `/explain <topic>` — Request grammar help

---

## 📁 Files

- `Modelfile` — Ollama model
- `streamlit_app.py` — Main app
- `docker-compose.yml` — ChromaDB
- `init_github.sh` — GitHub init script
