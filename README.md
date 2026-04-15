# NutriAI

**NutriAI** is an AI-powered supplement assistant that helps users explore products, get symptom-based recommendations, and chat with an intelligent nutrition-focused system in one place.

It combines semantic search, retrieval-aware responses, and a clean full-stack architecture:
- **Frontend:** React
- **Backend:** FastAPI
- **Database:** PostgreSQL + `pgvector`
- **Embeddings:** `sentence-transformers`
- **LLM layer:** Google GenAI

## Why This Project Is Interesting

NutriAI is more than a CRUD app with a chatbot bolted on top. It brings together:
- authenticated user flows
- vector similarity search over supplement embeddings
- chat memory with saved history and summaries
- fallback behavior when retrieval or database access fails
- a practical AI use case built around real product data

The result is a project that feels closer to a production-style AI assistant than a simple demo.

## Core Features

- User registration and login with JWT authentication
- Supplement catalog browsing
- Symptom-based supplement recommendations
- AI chat per logged-in user
- Saved chat history in the database
- Rolling conversation summaries for context preservation
- Graceful fallback responses when parts of the pipeline are unavailable

## Architecture

```text
NutriAI/
|-- Backend/
|   |-- main.py
|   |-- requirements.txt
|   `-- src/
|       |-- infrastructure/
|       |-- repositories/
|       |-- routers/
|       `-- services/
|-- Frontend/
|   `-- app/
|       |-- public/
|       `-- src/
`-- DataBase/
    |-- users.sql
    |-- supplements.sql
    |-- chat_history.sql
    |-- chat_summary.sql
    `-- data files
```

## Tech Stack

### Backend

- FastAPI
- SQLAlchemy
- PyJWT
- Uvicorn
- psycopg2

### AI and Retrieval

- sentence-transformers
- pgvector
- Google GenAI

### Frontend

- React 18
- Axios
- Tailwind tooling

## Environment Variables

Create a `.env` file inside `Backend/`:

```env
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/nutriai
SECRET_KEY=change_me
LLM_API_KEY=your_google_genai_api_key
LLM_MODEL=gemini-2.0-flash
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### Notes

- `DATABASE_URL` configures the SQLAlchemy connection.
- `SECRET_KEY` is used to sign JWT tokens.
- `LLM_API_KEY` is required for chat generation.
- `LLM_MODEL` defaults to `gemini-2.0-flash`.
- `EMBEDDING_MODEL` defaults to `all-MiniLM-L6-v2`.

## Database Setup

Run the SQL files from `DataBase/` on your PostgreSQL instance:

1. `users.sql`
2. `supplements.sql`
3. `chat_history.sql`
4. `chat_summary.sql`

Important details:
- `supplements.sql` enables the `vector` extension.
- supplement embeddings are stored as `VECTOR(384)`.
- recommendations rely on the `find_supplements(...)` SQL function.
- supplement records and embeddings still need to be imported into the `supplements` table.

## Local Development

### Backend

```powershell
cd Backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend default URL:

http://127.0.0.1:8000

### Frontend

```powershell
cd Frontend\app
npm install
npm start
```

Frontend default URL:

```text
http://localhost:3000
```

## API Overview

### Auth

- `POST /users/register`
- `POST /users/login`

Example:

```json
{
  "username": "demo",
  "password": "demo123"
}
```

### Supplements

- `GET /supplements`
- `GET /supplements/{name}`
- `GET /supplements/recommendations?symptoms=fatigue&symptoms=stress`

### Chat

- `POST /chat`
- requires `Authorization: Bearer <token>`

Example:

```json
{
  "text": "I feel tired and low on energy, what supplements may help?"
}
```

## How The Chat Flow Works

When a user sends a message:
- the system saves the message to chat history
- it loads recent history and an existing summary
- it builds context for the prompt
- it attempts a retrieval-aware answer
- if that fails, it falls back to a more general LLM response
- it stores the assistant reply
- it refreshes the conversation summary when needed

## Frontend Experience

After login, the app exposes three main views:
- **Supplements** for browsing the database
- **Recommendations** for symptom-based discovery
- **Chat** for AI conversation

The frontend stores the JWT token in `localStorage` and automatically attaches it to API requests.

## Common Issues

### Chat does not respond

Check that:
- `LLM_API_KEY` is set
- the database is reachable
- the required SQL tables exist
- you are logged in with a valid token

### Recommendations return empty results

Check that:
- the `supplements` table contains records
- the `embedding` column is populated
- `pgvector` is installed
- `find_supplements(...)` exists in the database

### Frontend cannot connect to backend

Check that:
- the backend is running on `http://127.0.0.1:8000`
- the frontend is running on `http://localhost:3000`
- no local port conflict is blocking either service

## Future Improvements

- add `Backend/.env.example`
- add an automated import pipeline for CSV supplement data
- add backend and frontend tests
- add Docker support for full local setup
- improve the UI and recommendation explainability
