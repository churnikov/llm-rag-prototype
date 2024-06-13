# llm-rag-prototype
LLM RAG Prototype


## Setup

### Build the docker image

    docker build -t llm-rag-prototype:dev .

### Run the docker image

    docker run -p 127.0.0.1:8000:8000 -t llm-rag-prototype:dev

Note: original port was 1416

### The REST API spec

Browse http://localhost:1416/docs#/


## Development from base image deepset/hayhooks

### Setup

    docker run --rm -p 1416:1416 -v $PWD/src/pipelines:/opt/pipelines "deepset/hayhooks:main"

If using .env file containing API keys

    docker run --env-file ./.env --rm -p 1416:1416 -v $PWD/pipelines:/opt/pipelines "deepset/hayhooks:main"

### Add pipelines

Create yaml pipelines in the ./src/pipelines/ dir

### REST API spec

Browse  http://localhost:1416/docs#/

### Usage during development

A simple POST request to verify access to the REST API:

curl -X 'POST' \
  'http://localhost:1416/test_pipeline_01' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_addition": {
    "value": 19
  }
}'


curl -X 'POST' \
  'http://localhost:1416/chat_with_website' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "converter": {
    "meta": {},
    "extraction_kwargs": {}
  },
  "fetcher": {
    "urls": [
      "https://www.scilifelab.se/"
    ]
  },
  "llm": {
    "generation_kwargs": {}
  },
  "prompt": {
    "template": "What is SciLifeLab?",
    "template_variables": {},
    "query": "What is SciLifeLab?"
  }
}'
