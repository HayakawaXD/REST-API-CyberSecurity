from flask import Blueprint, jsonify, request
from .models import Vulnerability
from . import db

bp = Blueprint('api', __name__)


@bp.route('/')
def home():
    return jsonify(message='Welcome to the Cybersecurity API!')


@bp.route('/vulnerabilities', methods=['GET'])
def get_vulnerabilities():
    vulnerabilities = Vulnerability.query.all()
    return jsonify([v.to_dict() for v in vulnerabilities])


@bp.route('/vulnerabilities/<int:id>', methods=['GET'])
def get_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if vuln:
        return jsonify(vuln.to_dict())
    return jsonify(error='Vulnerability not found'), 404


@bp.route('/vulnerabilities', methods=['POST'])
def add_vulnerability():
    data = request.get_json() or {}
    required = ('name', 'affected_system', 'severity')
    for f in required:
        if f not in data:
            return jsonify(error=f'Missing field: {f}'), 400
    new_vuln = Vulnerability(name=data['name'], affected_system=data['affected_system'], severity=data['severity'])
    db.session.add(new_vuln)
    db.session.commit()
    return jsonify(new_vuln.to_dict()), 201


@bp.route('/vulnerabilities/<int:id>', methods=['PUT'])
def update_vulnerability(id):
    data = request.get_json() or {}
    vuln = Vulnerability.query.get(id)
    if not vuln:
        return jsonify(error='Vulnerability not found'), 404
    vuln.name = data.get('name', vuln.name)
    vuln.affected_system = data.get('affected_system', vuln.affected_system)
    vuln.severity = data.get('severity', vuln.severity)
    db.session.commit()
    return jsonify(vuln.to_dict())


@bp.route('/vulnerabilities/<int:id>', methods=['DELETE'])
def delete_vulnerability(id):
    vuln = Vulnerability.query.get(id)
    if not vuln:
        return jsonify(error='Vulnerability not found'), 404
    db.session.delete(vuln)
    db.session.commit()
    return jsonify(message='Vulnerability was deleted!')
