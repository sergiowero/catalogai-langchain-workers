# CatalogAI LangChain Workers

A FastAPI-based worker service that processes product data using Google's Generative AI models, storing embeddings in Supabase for efficient semantic search and retrieval.

## Overview

This service is part of the CatalogAI ecosystem, designed to handle background processing of product data. It provides the following core functionalities:

- Generate embeddings for product data using Gemini AI
- Process image captions using Gemini 2.0 Flash
- Store embeddings and metadata in Supabase
- Manage processing queues for distributed workloads
- Optimize product descriptions using AI

## Project Structure

```
app/
├── api/       # API routes
├── models/    # Pydantic models
├── services/  # Service implementations
├── tasks/     # Background job tasks
├── usecases/  # Use cases for API routes
└── workflows/ # Workflow definitions
```

## Tech Stack

- Python 3.13.*
- FastAPI
- Pydantic
- Supabase
- Celery (for background tasks)
- Uvicorn (ASGI server)

## Code Style and Structure

- Write concise, technical Python code with accurate examples
- Use functional and declarative programming patterns; avoid classes
- Prefer iteration and modularization over code duplication
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError)
- Structure repository files as specified in the project structure

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd catalogai-langchain-workers
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with the required variables.

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### POST `/api/v1/tasks/{task_name}`
Execute a background task with the provided parameters.

**Request Body:**
```json
{
    "parameters": {
        "items_to_process": 5
    }
}
```

### GET `/api/v1/queues/embeddings`
Retrieve items currently in the embeddings queue.

**Response:**
```json
{
    "items": [...]
}
```

## Contributing

When contributing to this project, please follow these guidelines:

### Git Usage

Commit Message Prefixes:
- "fix:" for bug fixes
- "feat:" for new features
- "perf:" for performance improvements
- "docs:" for documentation changes
- "style:" for formatting changes
- "refactor:" for code refactoring
- "test:" for adding missing tests
- "chore:" for maintenance tasks

Rules:
- Use lowercase for commit messages
- Keep the summary line concise
- Include description for non-obvious changes
- Reference issue numbers when applicable

### Code Style

- Use functional methods for builders
- Favor type annotations
- Imports root is app
- Annotate return method types only if different from None
- Use ruff for formatting and linting

## License

This project is licensed under the MIT License - see the LICENSE file for details.