# My Python Project

This project is a FastAPI application that utilizes LangChain for creating embeddings with the Gemini model and stores them in Supabase. It is designed to provide a simple API for generating and managing embeddings, as well as interacting with a queue system for processing embedding jobs.

## Project Structure

```
my-python-project
├── app
│   ├── main.py              # Entry point of the FastAPI application
│   ├── api
│   │   └── routes.py        # API routes for handling requests
│   ├── services
│   │   ├── embeddings.py    # Logic for creating and saving embeddings
│   │   ├── queues.py        # Queue management services
│   │   └── captioning.py    # Image captioning logic
│   └── models
│       ├── product.py       # Product-related data models
│       └── queue.py         # Queue-related data models
├── .env                      # Environment variables for configuration
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
└── config.py                 # Configuration settings and environment loading
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd my-python-project
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory and add your Supabase API keys and other necessary configurations. Example:
   ```
   SUPABASE_URL=<your-supabase-url>
   SUPABASE_KEY=<your-supabase-key>
   ```

5. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Feature Flags

The application supports feature flags for enabling or disabling specific functionality. Currently, the following feature flag is available:

- `ENABLE_IMAGE_CAPTIONS`: Set to `true` to enable image captioning functionality. Defaults to `false`.

To enable this feature, add the following to your `.env` file:

```
ENABLE_IMAGE_CAPTIONS=true
```

## Usage

Once the application is running, you can access the API at `http://localhost:8000`. The API provides the following endpoints:

### POST `/api/v1/embeddings`
Generates embeddings for a specified number of items in the queue.

**Request Body:**
```json
{
    "items_to_process": 5
}
```

**Response:**
```json
{
    "message": "Embedding complete",
    "result": [...]
}
```

### GET `/api/v1/queues/embeddings`
Retrieves items currently in the embeddings queue.

**Response:**
```json
{
    "items": [...]
}
```

### OpenAPI Documentation
FastAPI automatically generates OpenAPI documentation for the application. You can access it at:

- Interactive API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Raw OpenAPI JSON: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the project. 

## License

This project is licensed under the MIT License. See the LICENSE file for more details.