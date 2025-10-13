from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Security.db"

db = SQLAlchemy(app)

class Vulnerability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    affected_system = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "affected_system": self.affected_system,
            "severity": self.severity
        }


with app.app_context():
    db.create_all()


# Routes
@app.route("/")
def home():
    return jsonify(message="Welcome to the Cybersecurity API!")


@app.route("/vulnerabilities", methods=["GET"])
def get_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    
    return jsonify([v.to_dict() for v in vulnerabilities])


@app.route("/vulnerabilities/<int:id>", methods=["GET"])
def get_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if vuln:
        return jsonify(vuln.to_dict())
    else:
        return jsonify(error="Vulnerability not found"), 404
 
# Post
@app.route("/vulnerabilities", methods=["POST"])
def add_vulnerability():
    data = request.get_json()
    new_vuln = Vulnerability(name=data["name"], affected_system=data["affected_system"], severity=data["severity"])
    db.session.add(new_vuln)
    db.session.commit()
    
    return jsonify(new_vuln.to_dict()), 201


# PUT -> Update
@app.route("/vulnerabilities/<int:id>", methods=["PUT"])
def update_vulnerability(id):
    data = request.get_json()
    vuln = Vulnerability.query.get(id)
    if vuln:
        vuln.name = data.get("name", vuln.name)
        vuln.affected_system = data.get("affected_system", vuln.affected_system)
        vuln.severity = data.get("severity", vuln.severity)
        db.session.commit()
        return jsonify(vuln.to_dict())
    else:
        return jsonify(error="Vulnerability not found"), 404


@app.route("/vulnerabilities/<int:id>", methods=["DELETE"])
def delete_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if vuln:
        db.session.delete(vuln)
        db.session.commit()
        return jsonify(message="Vulnerability was deleted!")
    else:
        return jsonify(error="Vulnerability not found"), 404


if __name__ == "__main__":
    app.run(debug=True)