# Semantic

## About

API that implements XLM-RoBERTa and FAISS as a semantic server

## Environment

FAISS index is trained and created separately.

Use `miniconda` to replicate the environment: `conda env create --file <file.yaml>`

Define the following environment variables:

- `SEMANTIC_PORT`
- `API_KEY`
- `FAISS_INDEX_PATH`
- `FAISS_UUIDS_PATH`
- `LOG_LEVEL`
- `LOG_PATH`
- `LOG_NAME`
