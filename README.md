
# Concierge AI

An AI-powered customer support assistant that answers questions using company documents, retrieves relevant information through semantic search, checks mock order details, and escalates unsupported questions to human support.

## Features

- PDF and TXT document ingestion
- Sentence-aware document chunking
- Semantic search using Sentence Transformers
- FAISS vector database
- Gemini-powered RAG responses
- Source metadata in answers
- Automatic human-support escalation
- Persistent escalation tickets using JSON
- Mock order lookup API
- Simulated slow, error and malformed API responses
- FastAPI REST endpoints
- Automated regression tests
- Offline retrieval evaluation

## Architecture

```text
Company Documents
       |
       v
Document Loader
       |
       v
Text Chunking
       |
       v
Sentence Transformers
       |
       v
FAISS Vector Index
       |
       v
Customer Question
       |
       v
Semantic Retrieval
       |
       v
Relevance Filtering
       |
       v
Gemini LLM
       |
       v
Grounded Answer + Sources
       |
       +------> Human Escalation
                    |
                    v
             JSON Ticket Storage
```

## Technology Stack

| Component      | Technology            |
|----------------|-----------------------|
| Language       |                Python |
| API Framework  |               FastAPI |
| LLM            |         Google Gemini |
| Embeddings     | Sentence Transformers |
| Vector Search  |                 FAISS |
| PDF Processing |               PyMuPDF |
| Validation     |              Pydantic |
| Testing        |                Pytest |
| Storage        |        JSON and FAISS |

## Project Structure

```text
concierge-ai/
├── app/
│   ├── api/
│   ├── ingestion/
│   ├── retrieval/
│   └── services/
├── data/
│   └── documents/
├── evaluation/
│   ├── questions.json
│   └── evaluate_retrieval.py
├── storage/
│   ├── index.faiss
│   ├── chunks.json
│   └── escalations.json
├── tests/
├── FAILURES.md
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/chidusurabhi123-collab/concierge-ai
cd concierge-ai
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
```

Build the document index using the ingestion pipeline before starting the application.

Run the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint                   |  Purpose                        |
|--------|----------------------------|---------------------------------|
| GET    | `/`                        | Application status              |
| GET    | `/health`                  | Health check                    |
| POST   | `/api/ask`                 | Ask a customer-support question |
| GET    | `/api/orders/{order_id}`   | Retrieve order details          |
| POST   | `/api/escalations`         | Create support ticket           |
| GET    | `/api/escalations`         | List support tickets            |

### Mock Order Failure Simulation

```text
GET /api/orders/ORD1001?simulate=slow
GET /api/orders/ORD1001?simulate=error
GET /api/orders/ORD1001?simulate=malformed
```

## Evaluation

Initial offline retrieval evaluation:

|    Metric       |   Result    |
|-----------------|-------------|
| Questions       | 40          |
| Accuracy        | 87.50%      |
| Precision       | 72.22%      |
| Recall          | 100%        |
| True Positives  | 13          |
| False Positives | 5           |
| True Negatives  | 22          |
| False Negatives | 0           |

These metrics measure retrieval decisions, not final answer correctness.

Run evaluation:

```bash
python -m evaluation.evaluate_retrieval
```

Run automated tests:

```bash
python -m pytest tests/ -v
```

Current regression test result: 8 passed.

## Known Limitations

- Retrieval threshold is currently fixed at 0.45.
- Evaluation dataset contains only 40 questions.
- Final answer correctness has not yet been independently evaluated.
- Gemini API free-tier quota can limit requests.
- Escalation storage uses JSON and is intended for a single-process demonstration.
- Mock order data is not connected to a real commerce system.

## Future Improvements

- Improve retrieval relevance and answer grounding.
- Add stronger adversarial input handling.
- Add order API timeout and retry policies.
- Introduce database-backed ticket management.
- Add automated answer-quality evaluation.
- Add observability for latency, errors and token usage.

## Project Status

Prototype implementation with working document retrieval, RAG responses, mock order lookup, human escalation, persistent ticket storage and offline regression evaluation.
