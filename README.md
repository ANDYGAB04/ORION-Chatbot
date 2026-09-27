# AstraRag-Chatbot

AstraRag-Chatbot is an agentic Retrieval-Augmented Generation (RAG) chatbot built to answer questions from a local document library using a modern AI stack. The project ingests PDFs, stores their embeddings in ChromaDB, retrieves the most relevant chunks, and uses a CrewAI-powered question-answering agent to produce grounded responses with references and reasoning.

This repository is designed around educational or knowledge-base PDFs and is especially well-suited for document Q&A use cases such as textbook study assistance, course content search, and domain-specific knowledge retrieval.

## Overview

The system consists of three main layers:

- Document ingestion pipeline: reads documents from a local folder, chunks them, and creates a vector store
- Backend API: exposes a chat endpoint that receives the conversation history and returns the answer, sources, tool usage, and rationale
- Frontend UI: a Streamlit chat interface that sends user prompts to the backend and displays responses

The project currently uses a biology textbook PDF set located in the `docs/` directory, but the ingestion workflow is generic and can be adapted for any PDF-based knowledge base.

## Features

- PDF ingestion and chunking using LlamaIndex
- Embedding generation with Hugging Face models
- Vector retrieval via ChromaDB
- Agent-based answer generation using CrewAI
- Groq-powered LLM integration for fast reasoning and answer generation
- FastAPI backend for API-based chatbot access
- Streamlit frontend for interactive chat
- Conversation-history-aware chat flow
- Source grounding and tool/rationale metadata in responses

## Tech Stack

- Python
- FastAPI
- Streamlit
- ChromaDB
- LlamaIndex
- CrewAI
- Hugging Face Embeddings
- Groq LLM
- Pydantic + Pydantic Settings
- Python-dotenv

## Project Structure

```text
AstraRag-Chatbot/
├── .gitignore
├── README.md
├── env_template.txt
├── requirements.txt
├── docs/
│   ├── 1. Sexual Reproduction in Flowering Plants.pdf
│   ├── 2. Human Reproduction.pdf
│   ├── ...
│   └── 13. Biodiversity and its Conservation.pdf
├── src/
│   ├── __init__.py
│   ├── agents_src/
│   │   ├── __init__.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   └── question_answer_agent.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── agent_settings.py
│   │   ├── crew.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── get_llm.py
│   │   │   └── llm_configuration.py
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   └── question_answer_task.py
│   │   └── tools/
│   │       ├── __init__.py
│   │       └── rag_qa_tool.py
│   ├── backend/
│   │   ├── __init__.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── chat.py
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── backend_settings.py
│   │   ├── main.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── chat.py
│   ├── frontend/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── config/
│   │       ├── __init__.py
│   │       └── frontend_settings.py
│   └── rag_doc_ingestion/
│       ├── __init__.py
│       ├── config/
│       │   └── doc_ingestion_settings.py
│       └── ingest_docs.py
└──
```

## How It Works

### 1. Document ingestion

The ingestion script (`src/rag_doc_ingestion/ingest_docs.py`) loads files from the configured `DOCUMENTS_DIR`, parses them into chunks, and stores embeddings in ChromaDB.

It uses:

- `SimpleDirectoryReader` to read all PDFs from the documents folder
- `SimpleNodeParser` to split documents into manageable chunks
- Hugging Face embeddings to encode each chunk
- ChromaDB persistent storage to save the vector database

### 2. Retrieval and answer generation

The question-answering agent uses a custom tool (`rag_query_tool`) to:

- connect to the Chroma vector store
- load the embedding model
- create a query engine
- retrieve the top matching document chunks for a user query
- return the answer plus source file names

The tool is then wrapped into a CrewAI agent that answers user questions in a conversational style.

### 3. API and UI

The FastAPI application exposes a `/chat/answer` endpoint that accepts chat history and returns structured JSON:

```json
{
  "answer": "...",
  "sources": ["..."],
  "tool_used": "...",
  "rationale": "..."
}
```

The Streamlit frontend sends the latest message and chat history to the backend and displays the result to the user.

## Installation

1. Clone the repository

```bash
git clone https://github.com/ANDYGAB04/AstraRag-Chatbot.git
cd AstraRag-Chatbot
```

2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Linux/macOS
# or
.venv\Scripts\activate      # On Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root using the template provided:

```bash
cp env_template.txt .env
```

Then update `.env` with your values:

```env
GROQ_API_KEY="your_groq_api_key"
DOCUMENTS_DIR="path/to/docs_dir"
VECTOR_STORE_DIR="path/to/doc_vector_store"
COLLECTION_NAME="document_collection"
MODEL_NAME="openai/gpt-oss-120b"
MODEL_TEMPERATURE=0.0
CHAT_ENDPOINT_URL="http://localhost:8000/chat/answer"
```

### Notes

- `GROQ_API_KEY` is required for the LLM used by the agent.
- `DOCUMENTS_DIR` should point to the folder containing your PDF files.
- `VECTOR_STORE_DIR` is where ChromaDB will persist its vector database.
- `COLLECTION_NAME` is the name of the Chroma collection used for document indexing.

## Running the Project

### 1. Build the vector store

Before using the chatbot, ingest the knowledge base:

```bash
python src/rag_doc_ingestion/ingest_docs.py
```

This creates the Chroma vector store based on the PDFs in `docs/` or whichever folder you configure.

### 2. Start the backend API

```bash
python src/backend/main.py
```

By default, the app runs on:

```text
http://localhost:8000
```

### 3. Start the Streamlit frontend

Open a second terminal and run:

```bash
streamlit run src/frontend/app.py
```

Then open the local Streamlit URL in your browser.

## Example Usage

Once the backend and frontend are running:

- Ask: “What is evolution?”
- Ask: “Explain human reproduction in simple terms.”
- Ask: “Compare ecosystem and biodiversity.”
- Ask: “What are the key points from the document about biotechnology?”

The system will retrieve the most relevant chunks from the indexed documents and generate a grounded response.

## API Endpoint

### POST `/chat/answer`

Request payload:

```json
{
  "chat_history": [
    {"role": "user", "content": "What is evolution?"},
    {"role": "assistant", "content": "Evolution is..."},
    {"role": "user", "content": "Explain it in more detail"}
  ]
}
```

Response example:

```json
{
  "answer": "Evolution is the change in heritable traits in populations over generations...",
  "sources": ["6. Evolution.pdf"],
  "tool_used": "RAG Retriever",
  "rationale": "The answer was selected from the most relevant chunks retrieved from the vector store."
}
```

## Customization

You can adapt this project for other document domains by:

- replacing the PDF folder in `docs/`
- updating `DOCUMENTS_DIR` in `.env`
- changing the embedding or LLM model in the config files
- modifying the agent goal and task instructions for a different use case

## Limitations

- The system depends on the quality and coverage of the indexed documents.
- Retrieval quality depends on chunk size and embedding model choice.
- Groq API quotas, rate limits, and credentials must be valid for the model to work.
- The current project is optimized for local document retrieval and not a large-scale multi-user production deployment.

## Future Improvements

- Add PDF OCR or text extraction for scanned documents
- Support multiple file types beyond PDFs
- Add authentication and user sessions
- Add logging, monitoring, and dashboards
- Support larger document corpora with better indexing strategies
- Add citation rendering with exact section references
- Improve evaluation and answer quality testing

## License

This project does not currently specify a license in the repository. If you plan to distribute or share it, you should add an appropriate open-source license file before public release.

## Contribution

Contributions are welcome. If you want to improve the project, you can:

- fix retrieval or answer quality issues
- improve the frontend UX
- add more robust configuration and deployment support
- document new features and workflows

## Contact

Repository: https://github.com/ANDYGAB04/AstraRag-Chatbot

If you are using this project for learning or experimentation, feel free to adapt it to your own knowledge-base use case.
