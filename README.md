# REST-API-CyberSecurity

Simple Flask API to manage vulnerabilities (CRUD).

Repository contents

- `CodeAPI.py` - original monolithic version of the API (starting point).
- `codeapi/` - modularized package containing the application:
  - `__init__.py` - factory and app initialization
  - `config.py` - configuration (SQLite)
  - `models.py` - `Vulnerability` model
  - `routes.py` - routes and API logic
- `run.py` - entry point to run the app (factory)
- `tests/` - automated tests using pytest
- `EXPLAIN.md`, `LINE_BY_LINE.md`, `CodeAPI_comentado.py` - documentation and detailed explanations

Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt` and `requirements-dev.txt`.

Installation (Windows PowerShell)


```powershell
cd "d:\VSCode\REST API"
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Running the application

```powershell
python run.py
# or
python CodeAPI.py
```

The API will be available at `http://127.0.0.1:5000/`.

Endpoints

- `GET /` — welcome message
- `GET /vulnerabilities` — list all vulnerabilities
- `GET /vulnerabilities/<id>` — get vulnerability by id
- `POST /vulnerabilities` — create a vulnerability (JSON: `name`, `affected_system`, `severity`)
- `PUT /vulnerabilities/<id>` — update a vulnerability (partial update allowed)
- `DELETE /vulnerabilities/<id>` — delete a vulnerability

Tests

```powershell
pytest
```

License

This project is licensed under the MIT License — see the included `LICENSE` file for the full text.

---

## Table of Contents

- Overview
- Project structure
- Data model
- Endpoints (description + examples)
- Installation and local run
- Tests
- Configuration and environment variables
- Database
- Security and best practices
- Deployment suggestions
- Contributing
- Troubleshooting / FAQ
- License

---

## Overview

This API implements basic CRUD operations for the `Vulnerability` resource. It was split from a single-file app (`CodeAPI.py`) into a modular package to improve maintainability: there is a `codeapi` package with an application factory (`create_app`), configuration, models and routes, plus a `run.py` script to start the app.

Project goals:
- Demonstrate a simple Flask + SQLAlchemy architecture
- Provide a starting point for studying security and REST APIs
- Include basic tests using pytest

---

## Project structure

(This structure was derived from the original single-file project)

- `CodeAPI.py` — original monolithic version kept for historical reference.
- `run.py` — entry point that loads the app factory and starts the server.
- `codeapi/` — main application package
  - `__init__.py` — application factory (`create_app`) and initialization of `db` (Flask-SQLAlchemy).
  - `config.py` — configuration (defaults to SQLite `Security.db`).
  - `models.py` — `Vulnerability` model and a `to_dict()` helper.
  - `routes.py` — blueprint with CRUD routes (list, get, create, update, delete).
- `requirements.txt` — runtime dependencies.
- `requirements-dev.txt` — development dependencies (pytest, etc.).
- `tests/` — automated tests (pytest).
- `EXPLAIN.md`, `LINE_BY_LINE.md`, `CodeAPI_comentado.py` — detailed documentation and a commented copy of the original file.
- `.gitignore` — ignores venvs, `Security.db`, and other local artifacts.

---

## Data model

Resource: Vulnerability

Fields (SQLAlchemy model `Vulnerability`):
- `id` (int, primary key) — unique identifier
- `name` (string) — vulnerability name/title
- `affected_system` (string) — target/affected system
- `severity` (string) — severity level (e.g. `low`, `medium`, `high`)

Helper: `to_dict()` — converts a model instance to a JSON-serializable dictionary.

---

## Endpoints

Base route: `/` (health check)

1) GET /
- Description: basic health endpoint that returns a simple message.
- Response (200):
  {
    "message": "API up and running"
  }

2) GET /vulnerabilities
- Description: list all saved vulnerabilities.
- Response (200): Array of Vulnerability objects.

Example response:
[
  {"id":1, "name":"SQL Injection", "affected_system":"app.example.com", "severity":"high"},
  {"id":2, "name":"XSS", "affected_system":"web.example.com", "severity":"medium"}
]

3) GET /vulnerabilities/<id>
- Description: return a single vulnerability by `id`.
- Response (200): Vulnerability object
- Error (404): when `id` does not exist.

4) POST /vulnerabilities
- Description: create a new vulnerability.
- Requires JSON body with at least `name`, `affected_system`, and `severity`.
- Response (201): the created object
- Error (400): missing fields or malformed request.

Example payload (JSON):
{
  "name": "Directory Traversal",
  "affected_system": "files.example.com",
  "severity": "high"
}

5) PUT /vulnerabilities/<id>
- Description: update an existing vulnerability. Accepts partial fields (`name`, `affected_system`, `severity`).
- Response (200): updated object
- Error (404): when `id` does not exist.

6) DELETE /vulnerabilities/<id>
- Description: permanently delete the vulnerability with `id`.
- Response (200): confirmation message
- Error (404): when `id` does not exist.

---

## Usage examples

Below are examples using PowerShell (Windows), curl (Linux/macOS/WSL), and Python (requests). Replace `http://127.0.0.1:5000` with your server host/port.

### PowerShell (Windows)

List vulnerabilities:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:5000/vulnerabilities
```

Create a vulnerability:

```powershell
$body = @{ name = 'Test Vuln'; affected_system = 'localhost'; severity = 'low' } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/vulnerabilities -Body $body -ContentType 'application/json'
```

Update (PUT):

```powershell
$body = @{ severity = 'medium' } | ConvertTo-Json
Invoke-RestMethod -Method Put -Uri http://127.0.0.1:5000/vulnerabilities/1 -Body $body -ContentType 'application/json'
```

Delete:

```powershell
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:5000/vulnerabilities/1
```

### curl (Linux / macOS / WSL)

List:

```bash
curl -s http://127.0.0.1:5000/vulnerabilities | jq
```

Create:

```bash
curl -X POST http://127.0.0.1:5000/vulnerabilities \
  -H "Content-Type: application/json" \
  -d '{"name":"Dir Traversal","affected_system":"files.example.com","severity":"high"}'
```

Update:

```bash
curl -X PUT http://127.0.0.1:5000/vulnerabilities/1 \
  -H "Content-Type: application/json" \
  -d '{"severity":"medium"}'
```

Delete:

```bash
curl -X DELETE http://127.0.0.1:5000/vulnerabilities/1
```

### Python (requests)

```python
import requests

BASE = 'http://127.0.0.1:5000'

# Create
payload = { 'name': 'Example', 'affected_system': 'app', 'severity': 'low' }
r = requests.post(f'{BASE}/vulnerabilities', json=payload)
print(r.status_code, r.json())

# List
r = requests.get(f'{BASE}/vulnerabilities')
print(r.status_code, r.json())
```

---

## Installation and local run (Windows - PowerShell)

1. Clone the repository:

```powershell
git clone https://github.com/HayakawaXD/REST-API-CyberSecurity.git "REST-API-CyberSecurity"
cd "REST-API-CyberSecurity"
```

2. Create a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> If PowerShell blocks script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` as administrator, or use `.
\.venv\Scripts\Activate.bat` in cmd.exe.

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the application (dev mode):

```powershell
python run.py
```

The app will be available by default at `http://127.0.0.1:5000` (Flask dev server). For production, see the deployment section.

---

## Tests

Tests use `pytest` and an in-memory SQLite database for isolation.

To run tests:

```powershell
# with venv activated
pip install -r requirements-dev.txt
pytest -q
```

Relevant files:
- `tests/test_api.py` — basic cases: empty GET, POST creation, required-field validation.
- `pytest.ini` — pytest configuration.

---

## Configuration and environment variables

Main settings can be adjusted in `codeapi/config.py` or via environment variables used when instantiating the app.

- `SQLALCHEMY_DATABASE_URI` — defaults to `sqlite:///Security.db`. You can export/set another URI, for example to use PostgreSQL during development:

```powershell
$env:SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/dbname'
python run.py
```

- `FLASK_ENV` / `FLASK_DEBUG` — control debug behavior (dev only).

Note: Do not store sensitive credentials in code. Use environment variables or secure config stores.

---

## Database and persistence

- By default the project uses SQLite: a `Security.db` file will be created in the project root.
- The `Vulnerability` model contains the fields described above.

Migrations: this project does not include migration tooling (Flask-Migrate) for simplicity. In production, add Flask-Migrate/Alembic to manage schema changes safely.

---

## Security and best practices

Important notes before using this code in production:
- Validation: current validation is minimal. For production, validate types, lengths and allowed values (e.g. `severity`).
- Authentication/Authorization: add authentication (JWT, OAuth2) for administrative endpoints.
- Rate limiting: protect endpoints with rate limiting (Flask-Limiter) to mitigate abuse.
- CORS: restrict CORS to trusted origins (Flask-CORS).
- Sanitize inputs: while SQLAlchemy reduces SQL injection risk, avoid raw SQL and sanitize any user-provided content.
- Logging: add structured logging and proper error tracking.

---

## Deployment suggestions

General recommendations:
- Do not use Flask's development server in production.
- On Linux, use Gunicorn (or uWSGI) behind Nginx.
- On Windows, consider Waitress or run inside WSL with Gunicorn.

Minimal Gunicorn example (Linux):

```bash
# inside the venv
pip install gunicorn
# run the app (assuming run.py exposes the app)
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

For Docker: create a Dockerfile that installs dependencies, copies the code, exposes the port and runs Gunicorn. Use multi-stage builds and avoid copying a local venv.

---

## Contributing

1. Fork the repository
2. Create a feature/bugfix branch: `git checkout -b feature/your-feature`
3. Make changes and include tests
4. Open a Pull Request describing the change

Suggested improvements:
- Add migrations with Flask-Migrate
- Add authentication (JWT)
- Improve validation (marshmallow or pydantic)
- Add CI (GitHub Actions) to run tests

---

## Troubleshooting / FAQ

Q: I get `sqlite3.OperationalError: unable to open database file`.
A: Check write permissions on the project directory and that the `SQLALCHEMY_DATABASE_URI` path is valid. On Windows, absolute paths with spaces can be problematic; use a correct URI such as `sqlite:///C:/path/to/Security.db`.

Q: `ModuleNotFoundError: No module named 'codeapi'` when running `python run.py`.
A: Run from the project root (where `run.py` is) or adjust `PYTHONPATH`. Activate the venv and ensure the package `codeapi` is in the current directory.

Q: How to clear the database data?
A: Stop the application and remove `Security.db` (backup first if needed). When restarted (and if `db.create_all()` runs), tables will be recreated, but there are no migration histories.
