from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instância do SQLAlchemy que será inicializada na factory do app
db = SQLAlchemy()


def create_app():
    """Factory que cria e configura a aplicação."""
    app = Flask(__name__)
    app.config.from_object('codeapi.config.Config')

    db.init_app(app)

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()

    return app
