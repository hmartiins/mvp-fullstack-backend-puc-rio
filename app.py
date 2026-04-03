import os

from flask import jsonify
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info
from pydantic import ValidationError

from model.models import db
from utils import format_pydantic_errors
from service.exceptions import NotFoundError, ConflictError
from routes.categorias import bp as categorias_bp
from routes.despesas import bp as despesas_bp


info = Info(
    title="Controle de Gastos Pessoais",
    version="1.0.0",
    description="API REST para registrar e consultar gastos pessoais organizados por categorias.",
)

app = OpenAPI(__name__, info=info, doc_prefix="/docs")
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'database', 'gastos.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.errorhandler(ValidationError)
def handle_validation_error(e: ValidationError):
    return jsonify({"erros": format_pydantic_errors(e.errors())}), 422


@app.errorhandler(NotFoundError)
def handle_not_found(e: NotFoundError):
    return jsonify({"erro": e.message}), 404


@app.errorhandler(ConflictError)
def handle_conflict(e: ConflictError):
    return jsonify({"erro": e.message}), 409


app.register_api(categorias_bp)
app.register_api(despesas_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("Banco de dados inicializado.")
    print("Swagger UI disponível em: http://localhost:5001/docs/swagger")
    app.run(debug=True, port=5001)
