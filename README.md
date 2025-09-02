# TheNewsCron 📰

**TheNewsCron** is an AI-powered news aggregation and publishing system designed for X (formerly Twitter).
It fetches fresh articles from external sources, evaluates their potential for engagement, and automatically generates X threads.

---

## 🚀 Features

- **News Aggregation** → Pulls in the latest articles from multiple news APIs.
- **Article Scoring** → Uses Gemini AI to assign a “virality score” to articles.
- **Thread Generation** → Converts long-form articles into concise, engaging X threads.
- **Embeddings & Vector Store** → Uses FAISS for semantic storage & retrieval.
- **Streamlit Dashboard** → Monitor and manage the pipeline with a simple UI.
- **Modular Design** → Independent modules for sources, scoring, embeddings, and storage.

---

## 📂 Project Structure

```
.
├── app.py                 # Streamlit dashboard
├── aggregator.py          # Collects and stores new articles
├── executor.py            # Scores articles and generates threads
├── run_aggregator.sh      # Cron/script runner for aggregator
├── run_executor.sh        # Cron/script runner for executor
│
├── embedder/              # Embedding logic
│   ├── base.py
│   └── gemini.py
│
├── articlescorer/         # AI-based scoring logic
│   ├── base.py
│   └── gemini.py
│
├── newssource/            # News fetchers
│   ├── base.py
│   └── newsdataio.py
│
├── vectorstore/           # Vector storage abstraction (FAISS)
│   ├── base.py
│   └── faiss.py
│
├── faiss_store            # FAISS index files
├── articles.csv           # Stored articles
├── threads.csv            # Generated threads
├── state.json             # Processing state (checkpoints)
│
├── config.py              # Project config
├── globals.py             # Shared constants
├── requirements.txt       # Python dependencies
└── .env                   # API keys and environment variables
```

---

## ⚙️ Setup

### 1. Clone & Install

```bash
git clone https://github.com/your-username/thenewscron.git
cd thenewscron
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file with required keys:

```ini
NEWSDATAIO_API_KEYS=your_news_api_key
GEMINI_API_KEYS=your_gemini_key
X_API_KEY=your_x_api_key
X_API_KEY_SECRET=your_x_api_key_secret
X_ACCESS_TOKEN=your_x_access_token
X_ACCESS_TOKEN_SECRET=your_x_access_token_secret
```

### 3. Data Storage

- **Articles** are stored in `articles.csv`
- **Threads** are stored in `threads.csv`
- **Embeddings** in `faiss_store`

---

## ▶️ Usage

### Run Aggregator (fetches articles)

```bash
python aggregator.py
```

### Run Executor (scores & generates threads)

```bash
python executor.py
```

### Streamlit Dashboard

```bash
streamlit run app.py
```

---

## 🔄 Automation

You can automate runs via **cron jobs**:

```bash
# Example: run every hour
0 * * * * /path/to/run_aggregator.sh
30 * * * * /path/to/run_executor.sh
```

---

## 🧩 Modules

- **`newssource/`** → Defines sources (e.g., NewsData.io)
- **`articlescorer/`** → AI models for scoring
- **`embedder/`** → Creates embeddings with Gemini
- **`vectorstore/`** → Manages FAISS index

Each module follows a `base.py` abstract structure for easy extensibility.

---

## 🛠️ Future Improvements

- Multi-source aggregation (RSS, GDELT, custom scrapers)
- Better scoring with fine-tuned models
- X API integration for **direct posting**
- Rich Streamlit dashboard (analytics, leaderboards)

---

## 📜 License

MIT License – feel free to use and modify.
