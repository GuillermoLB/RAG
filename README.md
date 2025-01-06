# RAG

## Overview

RAG (Retrieval-Augmented Generation) is a FastAPI-based application that leverages advanced natural language processing (NLP) techniques to provide question-answering capabilities. The application uses document extraction, text chunking, and vector embeddings to retrieve relevant information and generate responses.

## Features

- **Document Extraction**: Extracts text from PDF documents.
- **Text Chunking**: Splits documents into manageable chunks for processing.
- **Vector Embeddings**: Uses embeddings to represent text chunks for efficient retrieval.
- **Question Answering**: Generates responses to user queries based on retrieved context.
- **Authentication**: Provides token-based authentication for secure access.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.12
- PostgreSQL

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/rag.git
    cd rag
    ```

2. **Set up the virtual environment**:
    ```sh
    make create_environment
    source .venv/bin/activate
    ```

3. **Install dependencies**:
    ```sh
    make requirements
    ```

4. **Initialize the database**:
    ```sh
    make init_db
    ```

5. **Run the application**:
    ```sh
    make run
    ```

### Configuration

Update the [`.env`](.env ) file with your configuration settings:

SECRET_KEY=your_secret_key ALGORITHM=HS256 ACCESS_TOKEN_EXPIRE_MINUTES=30 DATA_FILE_PATH=data/your_document.pdf EMBED_MODEL_ID=sentence-transformers/all-MiniLM-L6-v2 RESPONSE_MODEL_ID=mistral POSTGRES_USER=user POSTGRES_PASSWORD=password POSTGRES_DB=db POSTGRES_HOST=localhost POSTGRES_PORT=5432

### Usage

- **Ingest a document**:
    ```sh
    curl -X POST "http://localhost:8000/documents/ingest" -H "Authorization: Bearer <your_token>"
    ```

- **Query the system**:
    ```sh
    curl -X POST "http://localhost:8000/query" -H "Authorization: Bearer <your_token>" -d "query=Who is Guillermo?"
    ```

### Testing

Run the tests using `pytest`:
```sh
pytest
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.



