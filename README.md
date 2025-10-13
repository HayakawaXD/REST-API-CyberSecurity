# REST-API-CyberSecurity

API simples em Flask para gerenciar vulnerabilidades (CRUD).

Conteúdo do repositório

- `CodeAPI.py` - versão monolítica original da API (ponto de partida).
- `codeapi/` - pacote modularizado com aplicação:
  - `__init__.py` - factory e inicialização do app
  - `config.py` - configurações (SQLite)
  - `models.py` - modelo `Vulnerability`
  - `routes.py` - rotas e lógica da API
- `run.py` - ponto de entrada para executar a app (factory)
- `tests/` - testes automatizados com pytest
- `EXPLAIN.md`, `LINE_BY_LINE.md`, `CodeAPI_comentado.py` - documentação e explicações detalhadas

Requisitos

- Python 3.8+
- Dependências listadas em `requirements.txt` e `requirements-dev.txt`.

Instalação (Windows PowerShell)

```powershell
cd "d:\VSCode\REST API"
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Executando a aplicação

```powershell
python run.py
# ou
python CodeAPI.py
```

A API ficará disponível em `http://127.0.0.1:5000/`.

Endpoints

- `GET /` — mensagem de boas-vindas
- `GET /vulnerabilities` — lista todas as vulnerabilidades
- `GET /vulnerabilities/<id>` — obtém vulnerabilidade por id
- `POST /vulnerabilities` — cria vulnerabilidade (JSON: `name`, `affected_system`, `severity`)
- `PUT /vulnerabilities/<id>` — atualiza vulnerabilidade (parcialmente permitido)
- `DELETE /vulnerabilities/<id>` — remove vulnerabilidade

Testes

```powershell
pytest
```

Notas e recomendações

- Em produção, remova `debug=True` e use um servidor WSGI (gunicorn/uwsgi).
- Use Flask-Migrate para migrações do banco em vez de `db.create_all()`.
- Valide entradas com Marshmallow/Pydantic antes de persistir.

Licença

Coloque a licença desejada (ex.: MIT) no repositório antes de tornar público.
