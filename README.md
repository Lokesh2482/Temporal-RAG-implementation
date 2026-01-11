# Temporal-RAG-implementation

Chronos-Audit is a time-aware forensic reasoning engine for verifying narrative
consistency between hypothetical backstory claims and long-form fictional texts.

Unlike traditional QA or fact-checking systems, Chronos-Audit treats silence as
non-contradiction and rejects claims only when explicit textual or physical
constraints are violated.

## Key Features

- Query-centric temporal reasoning (T^q)
- Hybrid sparse + dense retrieval
- Cross-encoder reranking
- Conservative tabula-rasa judgment
- Scalable ingestion via Pathway
- Grounded forensic evidence dossiers

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
