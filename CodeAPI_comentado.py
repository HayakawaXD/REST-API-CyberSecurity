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

    # Adiciona a nova instância à sessão e persiste no banco
    db.session.add(new_vuln)
    db.session.commit()
    
    # Retorna o recurso criado com código 201 (Created)
    return jsonify(new_vuln.to_dict()), 201


# PUT -> atualizar vulnerabilidade
@app.route("/vulnerabilities/<int:id>", methods=["PUT"])
def update_vulnerability(id):
    # Lê JSON do corpo (dados de atualização)
    data = request.get_json()
    # Busca o registro existente
    vuln = Vulnerability.query.get(id)
    if vuln:
        # Atualiza cada campo usando .get() para manter o valor atual se
        # o campo não for fornecido no JSON (permite updates parciais)
        vuln.name = data.get("name", vuln.name)
        vuln.affected_system = data.get("affected_system", vuln.affected_system)
        vuln.severity = data.get("severity", vuln.severity)
        # Persiste alterações
        db.session.commit()
        # Retorna o objeto atualizado
        return jsonify(vuln.to_dict())
    else:
        # Se não encontrado, retorna 404
        return jsonify(error="Vulnerability not found"), 404


# DELETE -> remover vulnerabilidade
@app.route("/vulnerabilities/<int:id>", methods=["DELETE"])
def delete_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if vuln:
        # Remove da sessão e comita para deletar do banco
        db.session.delete(vuln)
        db.session.commit()
        return jsonify(message="Vulnerability was deleted!")
    else:
        return jsonify(error="Vulnerability not found"), 404


# Bloco que permite executar este arquivo diretamente com `python CodeAPI_comentado.py`
# Observação: manter debug=True em produção é inseguro, pois mostra o debugger
# interativo em caso de exceções e pode vazar informações sensíveis.
if __name__ == "__main__":
    app.run(debug=True)
