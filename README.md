# RAG from Scratch

A document question-answering system that searches your documents and answers questions using their content.

## Overview

This system processes documents, stores them in a searchable format, and uses a language model to answer questions based on the retrieved content. It supports PDF, DOCX, and TXT files.

---

## Architecture

The system follows a Retrieval Augmented Generation (RAG) architecture with conversation history management. The diagram below illustrates the complete system flow:

### System Flow

1. **User Interaction**: Users initiate queries through a session interface
2. **Semantic Search**: The system performs semantic search against the indexed knowledge base (ChromaDB)
3. **Context Retrieval**: Relevant document chunks are retrieved based on semantic similarity
4. **Conversation History**: The last 10 conversation windows are fetched using session information
5. **Final Prompt Construction**: The system combines:
   - System Prompt
   - Conversation History (last 10 windows)
   - Retrieved Context
   - User Query
6. **LLM Processing**: The comprehensive prompt is sent to the Large Language Model
7. **Response Generation**: The LLM generates a response based on the provided context
8. **History Storage**: The conversation (query and response) is stored for future context

[![image.png](https://i.postimg.cc/3RnPMrMK/image.png)](https://postimg.cc/ZBvfpSKg)

---

### Document Ingestion Pipeline

The document ingestion process follows these steps:

1. **Load**: Raw documents (PDF, DOCX, TXT) are loaded from the data directory
2. **Split**: Documents are split into smaller chunks with overlap for better context preservation
3. **Embed**: Text chunks are converted into numerical vector embeddings using sentence transformers
4. **Store**: Embeddings and metadata are stored in ChromaDB for efficient semantic search

[![image.png](https://i.postimg.cc/dt7gXK5s/image.png)](https://postimg.cc/kBmj6Lrz)

---

## Features

- Document loading for PDF, DOCX, and TXT files
- Automatic text chunking with overlap
- Vector-based search using ChromaDB
- Support for multiple language model providers (Ollama, OpenAI, Groq)
- Conversation memory for context across multiple questions
- Automatic indexing of new documents

## Requirements

- Python 3.9 or higher
- Ollama (if using Ollama provider) - must be running locally on port 11434

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd rag-from-scratch
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Using Ollama (Default)

The default configuration uses Ollama. Make sure Ollama is installed and running:

```bash
# Install Ollama from https://ollama.ai
# Start Ollama service (usually runs automatically)
```

Edit `src/main.py` to change the model:
```python
llm = OllamaProvider(model="llama3")  # Change model name as needed
```

### Using OpenAI

1. Set your API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

2. Update `src/main.py`:
```python
from provider.openai_provider import OpenAIProvider
llm = OpenAIProvider(model="gpt-4o-mini")
```

### Using Groq

1. Install the Groq package:
```bash
pip install groq
```

2. Set your API key:
```bash
export GROQ_API_KEY="your-api-key-here"
```

3. Update `src/main.py`:
```python
from provider.groq_provider import GroqProvider
llm = GroqProvider(model="llama3.1:8b")
```

## Usage

1. Place your documents in the `data/` folder (PDF, DOCX, or TXT files).

2. Run the application:
```bash
python src/main.py
```

3. The system will automatically check and index any new documents in the `data/` folder.

4. Type your questions when prompted. Type `exit` or `quit` to end the session.

## Project Structure

```
rag-from-scratch/
├── data/                  # Place your documents here
├── src/
│   ├── ingest/           # Document loading and chunking
│   │   ├── loader.py     # File format loaders
│   │   └── chunker.py    # Text splitting logic
│   ├── vectorstore/      # ChromaDB integration
│   │   └── chroma_db.py  # Vector database operations
│   ├── provider/         # Language model providers
│   │   ├── base.py       # Base provider interface
│   │   ├── ollama_provider.py
│   │   ├── openai_provider.py
│   │   └── groq_provider.py
│   ├── memory/           # Conversation memory
│   │   └── chat_memory.py
│   ├── prompt/           # Prompt templates
│   │   └── prompt.py
│   └── main.py           # Main application entry point
├── storage/              # ChromaDB data storage
└── requirements.txt      # Python dependencies
```

## How It Works

1. **Document Processing**: Files in the `data/` folder are loaded and split into chunks of 500 characters with 50 character overlap.

2. **Indexing**: Text chunks are converted to embeddings and stored in ChromaDB with metadata about their source file.

3. **Search**: When you ask a question, the system searches for the 4 most relevant document chunks using semantic similarity.

4. **Answer Generation**: The retrieved chunks are combined with your question and sent to the language model, which generates an answer based on the provided context.

5. **Memory**: The conversation history is maintained to provide context for follow-up questions.

## Dependencies

- `chromadb` - Vector database for storing embeddings
- `sentence-transformers` - Embedding model (all-MiniLM-L6-v2)
- `PyPDF2` - PDF file reading
- `python-docx` - DOCX file reading
- `openai` - OpenAI API client (optional)

## Notes

- The vector database is stored in `storage/chroma_db/` and persists between sessions.
- Documents are only re-indexed if they are new or missing from the database.
- The system uses a sliding window memory that keeps the last 10 messages.
