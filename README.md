# llm-rag-prototype
LLM RAG Prototype


## Setup

### Build the docker image

    docker build -t llm-rag-prototype:dev .

### Run the docker image

    docker run -p 127.0.0.1:8000:8000 -t llm-rag-prototype:dev

Optionally get API keys from an .env file

    docker run --env-file ./src/.env --rm -p 127.0.0.1:8000:8000 -t llm-rag-prototype:dev

Note: original port was 1416

### The REST API spec

Browse http://localhost:8000/docs#/

Status http://localhost:8000/status


## API Keys

Some pipelines may require an API key. To use them, create env variables and set values accordingly:

* OPENAI_API_KEY


## Pipeline API endpoints

Interact with the API specification of the Chat with a website pipeline without using API tokens:

  /chat_with_website_spec

Chat with a website using model gpt-3.5-turbo:

  /chat_with_website

Chat with a wensite using model gpt-4:

  /chat_with_website_gpt4

Simple test pipeline:

  /test_pipeline_01


## Development from base image deepset/hayhooks

### Setup

    docker run --rm -p 1416:1416 -v $PWD/src/pipelines:/opt/pipelines "deepset/hayhooks:main"

If using .env file containing API keys

    docker run --env-file ./.env --rm -p 1416:1416 -v $PWD/pipelines:/opt/pipelines "deepset/hayhooks:main"

### Add pipelines

Create yaml pipelines in the ./src/pipelines/ dir

### REST API spec

Browse  http://localhost:1416/docs#/

Status: http://localhost:1416/status


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
