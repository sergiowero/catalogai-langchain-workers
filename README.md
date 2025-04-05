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
catalogai-langchain-workers
├── app
│   ├── main.py              # FastAPI application entry point
│   ├── api
│   │   └── routes.py        # API route definitions
│   ├── services
│   │   ├── embeddings.py    # Gemini embedding generation
│   │   ├── queues.py        # Queue management
│   │   ├── captioning.py    # Image captioning
│   │   └── summarize.py     # Product description optimization
│   ├── models
│   │   ├── product.py       # Product data models
│   │   ├── queue.py         # Queue data models
│   │   └── embeddings.py    # Embedding data models
│   ├── tasks
│   │   ├── database
│   │   │   └── tasks.py     # Database event handlers
│   │   └── product
│   │       └── tasks.py     # Product processing tasks
│   └── celeryapp.py         # Celery configuration
├── .env                     # Environment configuration
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── config.py                # Configuration management
```

## Requirements

- Python 3.8+
- FastAPI
- Google GenAI API
- Supabase
- Celery
- Uvicorn
- Pydantic

## Setup Instructions

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
   Create a `.env` file in the root directory with the following variables:
   ```
   SUPABASE_URL=<your-supabase-url>
   SUPABASE_KEY=<your-supabase-key>
   GOOGLE_API_KEY=<your-google-api-key>
   CELERY_BROKER_URL=amqp://celery:celery12345@74.208.70.103:5672/dev
   CELERY_BACKEND_URL=rpc://
   ```

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

## Task Organization

The project uses Celery for background task processing, with tasks organized into two main categories:

1. **Database Tasks** (`app/tasks/database/tasks.py`)
   - Handle database events and triggers
   - Manage embeddings job creation
   - Process product updates and deletions

2. **Product Tasks** (`app/tasks/product/tasks.py`)
   - Generate embeddings for products
   - Process image captions
   - Optimize product descriptions

## Development

The project uses FastAPI with async/await patterns for efficient background processing. It implements a queue-based architecture with Celery for distributed workloads, making it suitable for processing large volumes of product data.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.