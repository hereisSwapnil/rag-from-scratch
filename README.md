# RAG from Scratch

A document question-answering system that searches your documents and answers questions using their content.

## Overview

This system processes documents, stores them in a searchable format, and uses a language model to answer questions based on the retrieved content. It supports PDF, DOCX, and TXT files.

## 🎥 Demo

<!-- Add your demo video here -->

*Click the image above to watch the demo video*

## 📸 Screenshots

[![Clean-Shot-2025-11-17-at-03-04-02-2x.png](https://i.postimg.cc/x1NwhxRJ/Clean-Shot-2025-11-17-at-03-04-02-2x.png)](https://postimg.cc/87DXrbxN)


---

## Features

- Document loading for PDF, DOCX, and TXT files
- Automatic text chunking with overlap
- Vector-based search using ChromaDB
- Support for multiple language model providers (Ollama, OpenAI, Groq)
- Conversation memory for context across multiple questions
- Automatic indexing of new documents

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


## Requirements

- Python 3.9 or higher
- Ollama (if using Ollama provider) - must be running locally on port 11434

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rag-from-scratch
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Ollama (Default)

Make sure Ollama is installed and running. Edit `src/main.py`:
```python
llm = OllamaProvider(model="llama3")
```

### OpenAI

Set your API key and update `src/main.py`:
```bash
export OPENAI_API_KEY="your-api-key-here"
```
```python
from provider.openai_provider import OpenAIProvider
llm = OpenAIProvider(model="gpt-4o-mini")
```

### Groq

Install the package, set your API key, and update `src/main.py`:
```bash
pip install groq
export GROQ_API_KEY="your-api-key-here"
```
```python
from provider.groq_provider import GroqProvider
llm = GroqProvider(model="llama3.1:8b")
```

## Usage

1. Place your documents in the `data/` folder
2. Run the application:
```bash
python src/main.py
```
3. Ask questions when prompted. Type `exit` or `quit` to end.

## Project Structure

```
rag-from-scratch/
├── data/              # Place your documents here
├── src/
│   ├── ingest/       # Document loading and chunking
│   ├── vectorstore/  # ChromaDB integration
│   ├── provider/     # LLM providers (Ollama, OpenAI, Groq)
│   ├── memory/       # Conversation memory
│   ├── prompt/       # Prompt templates
│   └── main.py       # Main entry point
├── storage/          # ChromaDB data storage
└── requirements.txt
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

- Python 3.9+
- Ollama (if using Ollama provider)
