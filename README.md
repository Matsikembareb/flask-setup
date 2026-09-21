# Flask API

A Flask application scaffold with environment-based configuration, SQLAlchemy,
database migrations, CORS, JSON error responses, and OpenAPI documentation.

## Requirements

- Python 3.12 or newer
- Docker and Docker Compose (optional)
- A database URL for production

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in this directory when you need custom settings. Common
variables include:

```dotenv
FLASK_ENV=development
SECRET_KEY=change-me
JWT_SECRET_KEY=change-me
DATABASE_URL=sqlite:///development.db
CORS_ORIGINS=http://localhost:3000
```

The development configuration uses SQLite by default, so `DATABASE_URL` is
optional for local development. Testing always uses an in-memory SQLite
database. Production requires `DATABASE_URL`.

## Run Locally

Use the development configuration by default:

```bash
python3 run.py
```

Select an environment explicitly with the optional positional argument:

```bash
python3 run.py development
python3 run.py testing
python3 run.py production
```

The server listens on `http://localhost:5000`.

## Flask CLI

The project is compatible with `flask run` through the `app` object exported by
`wsgi.py`. Use the explicit app target from the project directory:

```bash
flask --app wsgi run
```

To select an environment, set `FLASK_ENV` in `.env` or in the shell:

```bash
FLASK_ENV=development flask --app wsgi run --debug
FLASK_ENV=testing flask --app wsgi run
FLASK_ENV=production flask --app wsgi run
```

`flask run` uses `127.0.0.1:5000` by default. To expose the server on all
interfaces, use `--host 0.0.0.0`.

For Gunicorn, the same module-level application is used:

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

## Tests

Run the test suite with:

```bash
pytest
```

Tests use the testing configuration and an in-memory database.

## Docker

Create a `.env` file with production values, then start the service:

```bash
docker compose up --build
```

The container runs Gunicorn on port `5000` and uses `FLASK_ENV=production`.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health/` | Basic index response |
| `GET` | `/health/health` | Liveness check |
| `GET` | `/health/docs` | Swagger UI |
| `GET` | `/health/openapi.json` | OpenAPI specification |

## Project Structure

```text
app/
  config/       Environment configuration classes
  db/           SQLAlchemy database setup and models
  modules/      Feature blueprints and routes
  tests/        Pytest fixtures and tests
  utils/        Shared application utilities
run.py          Local development entry point
wsgi.py         Gunicorn/WSGI entry point
```

To add an API feature, create a blueprint under `app/modules/` and register it
from `app/__init__.py`.