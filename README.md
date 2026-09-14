# Memory-Augmented RAG System

A production-ready RAG chatbot that combines four types of memory to answer questions intelligently — built on top of a boilerplate provided as part of the Full Stack GenAI Bootcamp Assignment 06.

---

## What I Built

This project extends the base boilerplate by replacing in-memory demo stores with real production databases:

| Component | Original | Replaced With |
|-----------|----------|---------------|
| Short-term memory | Python dict (resets on restart) | **Redis Cloud** |
| Vector store (Semantic + RAG) | NumPy cosine similarity (in-memory) | **Qdrant Cloud** |
| Long-term memory | SQLite | SQLite (kept — valid for this scale) |

---

## Architecture

```
Current Query
    |
    +--> Short-Term Memory   (Redis — recent session messages)
    +--> Long-Term Memory    (SQLite — explicit user facts)
    +--> Semantic Memory     (Qdrant — similar past interactions)
    +--> RAG Knowledge Base  (Qdrant — domain documents)
              |
              v
         Context Fusion
              |
              v
             LLM
              |
              v
            Answer
              |
              +--> Update short-term memory (Redis)
              +--> Update semantic memory (Qdrant)
              +--> Save to long-term memory if user writes: Remember: ...
```

---

## Four Memory Types

**Short-Term Memory (Redis)**
Stores the last 6 messages of the current session. Uses Redis Lists with `rpush` and `ltrim`. Persists across restarts within the same session.

**Long-Term Memory (SQLite)**
Stores user facts and preferences explicitly. Triggered when user writes `Remember: ...`. Persists forever across all sessions.

**Semantic Memory (Qdrant)**
Stores past user interactions as embeddings. Retrieved by cosine similarity when a new query is similar to a past exchange. Helps the agent recall relevant previous conversations.

**RAG Knowledge Base (Qdrant)**
Stores domain documents as embeddings. Retrieved by cosine similarity to answer factual questions. In this demo: HR policy documents (leave policy, probation period, reimbursement rules).

---

## Tech Stack

- **LLM:** OpenAI `gpt-4.1-mini` (or any OpenAI-compatible model via `OPENAI_BASE_URL`)
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Short-term memory:** Redis Cloud
- **Long-term memory:** SQLite
- **Vector store:** Qdrant Cloud (cosine similarity, 384-dim vectors)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/memory-augmented-rag-assignment.git
cd memory-augmented-rag-assignment
```

### 2. Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # macOS/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your-openai-key (I'm using an API key from OpenRouter instead of an OpenAI API key.)
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=meta-llama/llama-3.1-8b-instruct
REDIS_HOST=your-redis-host
REDIS_PORT=your-redis-port
REDIS_PASSWORD=your-redis-password
QDRANT_URL=your-qdrant-cluster-url
QDRANT_API_KEY=your-qdrant-api-key
MAX_RECENT_MESSAGES=6
TOP_K_DOCUMENTS=3
TOP_K_MEMORIES=3
```

### 5. Run offline tests

```bash
python self_test.py
```

Expected output:
```
ALL OFFLINE TESTS PASSED
```

### 6. Run the app

```bash
python main.py
```

---

## Example Usage

```
Enter user_id [sunny_123]: yash_123
Enter session_id [session_1]: session_1

You: How long is the probation period?
AI: The probation period is six months.

You: Remember: I prefer concise bullet point answers
AI: Understood. I will save that as a long-term memory.

You: How many paid leaves do employees get?
AI: • Employees receive 20 paid leaves per year after completing probation.

You: What are my preferences?
AI: Based on your saved memory:
    • You prefer concise bullet point answers.
```

---

## Files Changed

| File | What Changed |
|------|-------------|
| `main.py` | Added `load_dotenv()` at top |
| `llm_service.py` | Switched to `chat.completions` API, added configurable `base_url` |
| `short_term_memory.py` | Replaced Python dict with Redis Cloud |
| `vector_store.py` | Replaced NumPy with Qdrant Cloud |
| `config.py` | Added Redis and Qdrant config variables |

---

## Production Database Options

| Component | Used Here | Production Alternatives |
|-----------|-----------|------------------------|
| Short-term memory | Redis Cloud | Redis Cluster, DynamoDB, MongoDB |
| Long-term memory | SQLite | PostgreSQL, MongoDB, DynamoDB |
| Semantic + RAG | Qdrant Cloud | pgvector, Pinecone, Weaviate, Milvus |

---

## Notes

- The `self_test.py` uses fake mode — it does not require API keys and tests offline logic only
- Qdrant collection is created automatically on first run
- Redis keys use `session_key` format to isolate different user sessions