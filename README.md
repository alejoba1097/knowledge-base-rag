# 📚 Knowledge Base RAG

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload documents and ask questions about their content. The system extracts text from documents, generates embeddings, stores them in a vector database, and uses an LLM to provide contextual, source-grounded answers.

![RAG Knowledge Base](https://img.shields.io/badge/RAG-Knowledge%20Base-blue?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)

### Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F61?style=for-the-badge&logo=databricks&logoColor=white)

### ML & NLP
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black)
![Sentence Transformers](https://img.shields.io/badge/Sentence%20Transformers-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Tesseract OCR](https://img.shields.io/badge/Tesseract-5C5C5C?style=for-the-badge&logo=google&logoColor=white)

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│    Frontend     │────▶│    Backend      │────▶│    ChromaDB     │
│  React + Vite   │     │    FastAPI      │     │  Vector Store   │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
             ┌──────────┐ ┌──────────┐ ┌──────────┐
             │Tesseract │ │ Sentence │ │  LLM     │
             │   OCR    │ │Transformers│ │(TinyLlama)│
             └──────────┘ └──────────┘ └──────────┘
```

The project follows **Clean Architecture** principles with clear separation of concerns:

- **Domain Layer**: Core business entities and repository interfaces
- **Application Layer**: Use cases (chat, upload document)
- **Infrastructure Layer**: External service implementations (ChromaDB, Sentence Transformers, Tesseract)
- **Interface Layer**: API controllers and schemas

---

## ✨ Features

- 📄 **Document Upload**: Upload PDF files and images
- 🔍 **Text Extraction**: Automatic OCR using Tesseract for text extraction
- 🧠 **Semantic Search**: Vector embeddings with Sentence Transformers
- 💬 **Chat Interface**: Ask questions and get contextual answers
- 📚 **Source Attribution**: Answers include references to source documents
- 🐳 **Containerized**: Full Docker Compose setup for easy deployment
- 🎮 **GPU Support**: NVIDIA GPU acceleration for faster inference

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- NVIDIA GPU with CUDA support (optional, for GPU acceleration)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) (if using GPU)

### Running with Docker Compose

1. **Clone the repository**
   ```bash
   git clone https://github.com/alejoba1097/knowledge-base-rag.git
   cd knowledge-base-rag
   ```

2. **Start all services**
   ```bash
   docker compose up --build
   ```

3. **Access the application**
   - Frontend: http://localhost:4173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Running without GPU

If you don't have an NVIDIA GPU, modify the `docker-compose.yml` to remove the GPU configuration:

```yaml
backend:
  build:
    context: .
    dockerfile: backend/Dockerfile
  environment:
    KB_CHROMA_HOST: chroma
    KB_CHROMA_PORT: 8000
    KB_CHROMA_COLLECTION_NAME: documents
    KB_RAG_MODEL_NAME: TinyLlama/TinyLlama-1.1B-Chat-v1.0
  ports:
    - "8000:8000"
  depends_on:
    - chroma
  # Remove the gpus section
```

---

## 🔧 Local Development

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### ChromaDB (Vector Store)

```bash
docker run -d -p 8001:8000 ghcr.io/chroma-core/chroma:latest
```

---

## 📁 Project Structure

```
knowledge-base-rag/
├── backend/
│   ├── src/app/
│   │   ├── application/       # Use cases
│   │   │   ├── chat.py
│   │   │   └── upload_document.py
│   │   ├── core/              # Configuration
│   │   │   └── config.py
│   │   ├── domain/            # Business logic
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── services/
│   │   ├── infrastructure/    # External services
│   │   │   ├── embeddings/
│   │   │   ├── rag/
│   │   │   ├── text_extraction/
│   │   │   └── vectorstores/
│   │   ├── interfaces/        # API layer
│   │   │   └── api/
│   │   └── main.py
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatPanel.tsx
│   │   │   └── UploadPanel.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/upload` | Upload a document (PDF/image) |
| `POST` | `/chat` | Send a question and get an answer |
| `GET`  | `/docs` | OpenAPI documentation |

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `KB_CHROMA_HOST` | ChromaDB host | `chroma` |
| `KB_CHROMA_PORT` | ChromaDB port | `8000` |
| `KB_CHROMA_COLLECTION_NAME` | Collection name | `documents` |
| `KB_RAG_MODEL_NAME` | LLM model name | `TinyLlama/TinyLlama-1.1B-Chat-v1.0` |

---

## 📝 License

This project is licensed under the MIT License.

