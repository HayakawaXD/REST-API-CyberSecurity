# Código original comentado linha-a-linha (em português)

from flask import Flask, jsonify, request  # importa Flask e utilitários para JSON e requisições
from flask_sqlalchemy import SQLAlchemy  # integra SQLAlchemy ao Flask

# Cria a aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados: usa SQLite apontando para o arquivo Security.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Security.db"

# Instancia o SQLAlchemy vinculando à app
db = SQLAlchemy(app)


# Definição do modelo Vulnerability (tabela no banco)
class Vulnerability(db.Model):
    # id: chave primária inteira
    id = db.Column(db.Integer, primary_key=True)
    # name: nome da vulnerabilidade (string até 100 caracteres), não nulo
    name = db.Column(db.String(100), nullable=False)
    # affected_system: qual sistema é afetado (string até 100 chars), não nulo
    affected_system = db.Column(db.String(100), nullable=False)
    # severity: severidade como número (float), não nulo
    severity = db.Column(db.Float, nullable=False)

    def to_dict(self):
        # Converte a instância do modelo para um dicionário Python simples
        # Isso facilita serializar para JSON com jsonify
        return {
            "id": self.id,
            "name": self.name,
            "affected_system": self.affected_system,
            "severity": self.severity
        }


# Cria as tabelas no banco se não existirem (apenas para desenvolvimento simples).
# Em produção, prefira usar migrações (Flask-Migrate/Alembic) em vez de create_all.
with app.app_context():
    db.create_all()


# Rotas da API
@app.route("/")
def home():
    # Rota raiz que retorna uma mensagem de boas-vindas em JSON
    return jsonify(message="Welcome to the Cybersecurity API!")


@app.route("/vulnerabilities", methods=["GET"])
def get_vulnerabilities():
    # Busca todas as vulnerabilidades na tabela
    vulnerabilities = Vulnerability.query.all()
    # Retorna uma lista de dicionários (um por vulnerabilidade)
    return jsonify([v.to_dict() for v in vulnerabilities])


@app.route("/vulnerabilities/<int:id>", methods=["GET"])
def get_vulnerability(id):
    # Busca uma vulnerabilidade pelo ID (chave primária)
    vuln = Vulnerability.query.get(id)
    if vuln:
        # Se encontrada, retorna o objeto serializado
        return jsonify(vuln.to_dict())
    else:
        # Se não encontrada, retorna erro 404 com mensagem
        return jsonify(error="Vulnerability not found"), 404
 
# POST -> criar nova vulnerabilidade
@app.route("/vulnerabilities", methods=["POST"])
def add_vulnerability():
    # Lê o JSON enviado no corpo da requisição
    data = request.get_json()

    # Observação: aqui não há validação robusta. Se `data` for None ou
    # campos estiverem faltando, isso levantará uma exceção KeyError.
    # Em produção valide os dados antes de usá-los.
    new_vuln = Vulnerability(name=data["name"], affected_system=data["affected_system"], severity=data["severity"])

    # Original code commented line-by-line (translated to English)

    from flask import Flask, jsonify, request  # import Flask and helpers for JSON and requests
    from flask_sqlalchemy import SQLAlchemy  # integrate SQLAlchemy with Flask

    # Create the Flask application
    app = Flask(__name__)

    # Database configuration: use SQLite pointing to file Security.db
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Security.db"

    # Instantiate SQLAlchemy and bind it to the app
    db = SQLAlchemy(app)


    # Definition of the Vulnerability model (table in the database)
    class Vulnerability(db.Model):
        # id: integer primary key
        id = db.Column(db.Integer, primary_key=True)
        # name: vulnerability name (string up to 100 chars), not nullable
        name = db.Column(db.String(100), nullable=False)
        # affected_system: which system is affected (string up to 100 chars), not nullable
        affected_system = db.Column(db.String(100), nullable=False)
        # severity: severity as a number (float), not nullable
        severity = db.Column(db.Float, nullable=False)

        def to_dict(self):
            # Convert the model instance to a plain Python dict
            # This makes it easy to serialize to JSON with jsonify
            return {
                "id": self.id,
                "name": self.name,
                "affected_system": self.affected_system,
                "severity": self.severity
            }


    # Create tables in the database if they do not exist (for simple development).
    # In production, prefer using migrations (Flask-Migrate/Alembic) instead of create_all.
    with app.app_context():
        db.create_all()


    # API routes
    @app.route("/")
    def home():
        # Root route that returns a simple welcome message in JSON
        return jsonify(message="Welcome to the Cybersecurity API!")


    @app.route("/vulnerabilities", methods=["GET"])
    def get_vulnerabilities():
        # Fetch all vulnerabilities from the table
        vulnerabilities = Vulnerability.query.all()
        # Return a list of dictionaries (one per vulnerability)
        return jsonify([v.to_dict() for v in vulnerabilities])


    @app.route("/vulnerabilities/<int:id>", methods=["GET"])
    def get_vulnerability(id):
        # Fetch a vulnerability by ID (primary key)
        vuln = Vulnerability.query.get(id)
        if vuln:
            # If found, return the serialized object
            return jsonify(vuln.to_dict())
        else:
            # If not found, return a 404 error with a message
            return jsonify(error="Vulnerability not found"), 404

    # POST -> create a new vulnerability
    @app.route("/vulnerabilities", methods=["POST"])
    def add_vulnerability():
        # Read the JSON sent in the request body
        data = request.get_json()

        # Note: there is no robust validation here. If `data` is None or
        # fields are missing, this will raise a KeyError. In production validate
        # data before using it.
        new_vuln = Vulnerability(name=data["name"], affected_system=data["affected_system"], severity=data["severity"])

        # Add the new instance to the session and persist to the database
        db.session.add(new_vuln)
        db.session.commit()
    
        # Return the created resource with HTTP 201 (Created)
        return jsonify(new_vuln.to_dict()), 201


    # PUT -> update vulnerability
    @app.route("/vulnerabilities/<int:id>", methods=["PUT"])
    def update_vulnerability(id):
        # Read JSON from the body (update data)
        data = request.get_json()
        # Fetch the existing record
        vuln = Vulnerability.query.get(id)
        if vuln:
            # Update each field using .get() to preserve current value if
            # the field is not provided in the JSON (allows partial updates)
            vuln.name = data.get("name", vuln.name)
            vuln.affected_system = data.get("affected_system", vuln.affected_system)
            vuln.severity = data.get("severity", vuln.severity)
            # Persist changes
            db.session.commit()
            # Return the updated object
            return jsonify(vuln.to_dict())
        else:
            # If not found, return 404
            return jsonify(error="Vulnerability not found"), 404


    # DELETE -> remove vulnerability
    @app.route("/vulnerabilities/<int:id>", methods=["DELETE"])
    def delete_vulnerability(id):
        vuln = Vulnerability.query.get(id)
        if vuln:
            # Remove from the session and commit to delete from the database
            db.session.delete(vuln)
            db.session.commit()
            return jsonify(message="Vulnerability was deleted!")
        else:
            return jsonify(error="Vulnerability not found"), 404


    # Block that allows running this file directly with `python CodeAPI_comentado.py`
    # Note: leaving debug=True in production is insecure because it exposes the
    # interactive debugger on exceptions and may leak sensitive information.
    if __name__ == "__main__":
        app.run(debug=True)
