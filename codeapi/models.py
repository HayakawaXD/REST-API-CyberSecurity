from . import db


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
            "severity": self.severity,
        }
