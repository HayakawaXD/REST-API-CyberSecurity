DETAILED EXPLANATIONS (originally in Portuguese)

This file explains the modularized project created from the original `CodeAPI.py`.

Files created:

- `codeapi/__init__.py` - application factory `create_app()` and SQLAlchemy initialization
- `codeapi/config.py` - configuration (SQLite URI)
- `codeapi/models.py` - `Vulnerability` model
- `codeapi/routes.py` - blueprint with CRUD routes
- `run.py` - application entry point
- `CodeAPI_comentado.py` - commented copy of the original code
- `LINE_BY_LINE.md` - line-by-line explanations
- `tests/test_api.py` - basic tests

Suggestions:
- Use `python run.py` to start the application in development mode.
- For production, consider adding Flask-Migrate, authentication, and input validation.
