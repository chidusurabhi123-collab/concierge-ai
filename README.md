# Concierge AI

**Grounded AI customer support with semantic retrieval, order lookup, and human escalation.**

## 1. Project overview

Concierge AI is a prototype customer-support assistant designed to answer customer questions using company documents, retrieve supporting passages, look up mock order information, and escalate questions when the available information is insufficient.

The central design principle is: **the assistant should not invent company policies or claim information that its sources do not support.**

This project was developed for the EduRankAI three-day intern challenge, Project Concierge.

## 2. Features implemented

- PDF and TXT document loading using PyMuPDF.
- Sentence-aware text chunking.
- Text embeddings using Sentence Transformers (`all-MiniLM-L6-v2`).
- Semantic retrieval using FAISS.
- Saved vector index and chunk metadata.
- Gemini-powered question answering using retrieved context.
- Source metadata returned with answers.
- Relevance filtering using a provisional similarity threshold of 0.45.
- Human-support escalation for questions with no sufficiently relevant retrieved chunks or detected model refusals.
- Persistent escalation tickets stored in JSON.
- Mock order lookup API.
- Simulated slow, error, and malformed order-service responses.
- FastAPI endpoints and a browser-based customer-support dashboard.
- Offline retrieval evaluation and automated service tests.

## 3. Architecture

```text
                 COMPANY DOCUMENTS
                         |
                         v
                  Document Loader
                         |
                         v
                   Text Chunker
                         |
                         v
                Sentence Transformer
                         |
                         v
                    FAISS Index
                         |
                         v
CUSTOMER QUESTION --> Retrieval
                         |
                         v
                 Similarity Filter
                         |
                         v
                    Gemini LLM
                         |
                 +-------+-------+
                 |               |
                 v               v
          Grounded Answer    Human Escalation
          + Source Metadata       |
                                  v
                           JSON Ticket Store

CUSTOMER ORDER QUERY --> Mock Order Service
                              |
                              v
                         Order Response

                 FastAPI + Web Dashboard
```

## 4. Technology stack

| Layer | Technology |
|---|---|
| Backend language | Python 3.12 |
| API | FastAPI |
| Language model | Google Gemini API |
| Embeddings | Sentence Transformers |
| Vector search | FAISS |
| PDF extraction | PyMuPDF |
| Data validation | Pydantic |
| Frontend | HTML, CSS, JavaScript |
| Ticket persistence | JSON |
| Automated testing | Pytest |
| Development environment | Ubuntu on WSL, VS Code |

## 5. Project structure

```text
concierge-ai/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   ├── order_routes.py
│   │   └── escalation_routes.py
│   ├── ingestion/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   └── pipeline.py
│   ├── retrieval/
│   │   └── vector_store.py
│   ├── services/
│   │   ├── rag.py
│   │   ├── order_service.py
│   │   └── escalation_service.py
│   └── main.py
├── data/
│   └── documents/
├── evaluation/
│   ├── questions.json
│   └── evaluate_retrieval.py
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
├── storage/
│   ├── index.faiss
│   ├── chunks.json
│   └── escalations.json
├── tests/
│   └── test_services.py
├── FAILURES.md
├── README.md
└── requirements.txt
```

## 6. Setup and execution

### Prerequisites

- Python 3.12
- Git
- A Google Gemini API key

### Clone the repository

```bash
git clone  https://github.com/chidusurabhi123-collab/concierge-ai
cd concierge-ai
```

### Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Configure the API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit `.env` or expose the API key.

### Start the application

The repository includes the saved FAISS index and chunk metadata.

```bash
uvicorn app.main:app --reload
```

Open the dashboard:

`http://127.0.0.1:8000/`

Open interactive API documentation:

`http://127.0.0.1:8000/docs`

Health check:

`http://127.0.0.1:8000/health`

## 7. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Serve the dashboard |
| GET | `/health` | Health check |
| POST | `/api/ask` | Ask a question |
| GET | `/api/orders/{order_id}` | Look up an order |
| POST | `/api/escalations` | Create a support ticket |
| GET | `/api/escalations` | List escalation tickets |

### Example: ask a question

```json
{
  "question": "What is the refund policy?"
}
```

### Example: order lookup

```text
GET /api/orders/ORD1001
```

### Simulated order-service failures

```text
GET /api/orders/ORD1001?simulate=slow
GET /api/orders/ORD1001?simulate=error
GET /api/orders/ORD1001?simulate=malformed
```

The mock service simulates delayed responses, service errors, and malformed data to test API handling.

## 8. Evaluation

An initial offline evaluation was conducted using 40 questions.

| Metric               |    Result |
|----------------------|----------:|
| Evaluation questions |        40 |
| True positives       | 13        |
| False positives      | 5         |
| True negatives       | 22        |
| False negatives      | 0         |
| Decision accuracy    | 87.50%    |
| Precision            | 72.22%    |
| Recall               | 100.00%   |

These results measure whether the retrieval system returned at least one chunk above the 0.45 similarity threshold. They do **not** measure final answer correctness, factual grounding, or end-to-end safety.

Run the evaluation:

```bash
python -m evaluation.evaluate_retrieval
```

## 9. Automated tests

Run:

```bash
python -m pytest tests/ -v
```

Initial regression test result:

**8 tests passed.**

The tests cover valid and invalid order lookups, simulated service errors, malformed responses, ticket creation, queue retrieval, and unique ticket identifiers.

## 10. Known limitations and risks

- The evaluation dataset has 40 questions and needs stronger answer/source annotations and broader coverage.
- The similarity threshold is provisional and has not been systematically optimized.
- Semantic retrieval can find related policy passages even when those passages do not support the customer's specific claim.
- Final answer correctness has not yet been independently scored across the full dataset.
- The refusal detector uses phrase matching and is not a robust semantic verification mechanism.
- The mock order service is not connected to a real commerce platform.
- Order lookup is available as an API/dashboard feature; a complete order-aware conversational workflow is not yet implemented.
- The simulated slow endpoint waits five seconds but does not yet demonstrate a client-side timeout/retry policy.
- Ticket persistence uses JSON and is intended for a single-process demonstration, not concurrent production traffic.
- Gemini free-tier quota limits can temporarily prevent AI responses.
- The project has not been validated against a production workload.

## 11. Future improvements

With two additional weeks, the next priorities would be:

1. Add document versioning, contradiction detection, and incremental re-indexing.
2. Improve evaluation labels with correct answers and source passages.
3. Evaluate answer faithfulness and citation correctness separately from retrieval.
4. Add stronger adversarial and prompt-injection tests.
5. Integrate order lookup into the conversational workflow with validation and authorization.
6. Add timeout, retry, and circuit-breaker behavior for external services.
7. Move ticket persistence to PostgreSQL.
8. Add latency, token usage, cost, and failure monitoring.
9. Compare at least two retrieval/model configurations on the same evaluation set.

## 12. AI assistance disclosure

AI coding assistance was used during development for implementation guidance, debugging, code drafting, and documentation. The project code and design decisions should be reviewed and explained by the developer during the technical walkthrough.

## 13. Project status

Concierge AI is a working prototype with document ingestion, semantic retrieval, LLM-based responses, source metadata, mock order lookup, human escalation, persistent ticket storage, automated service tests, and a web dashboard.

It is a prototype, not a production-ready customer-support system.
