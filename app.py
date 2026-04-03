import os

from flask import Flask
from flask_cors import CORS
from flasgger import Swagger

from model.models import db
from swagger_config import SWAGGER_TEMPLATE, SWAGGER_CONFIG
from routes.categorias import bp as categorias_bp
from routes.despesas import bp as despesas_bp

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'database', 'gastos.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

Swagger(app, template=SWAGGER_TEMPLATE, config=SWAGGER_CONFIG)

app.register_blueprint(categorias_bp)
app.register_blueprint(despesas_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("Banco de dados inicializado.")
    print("Documentação Swagger disponível em: http://localhost:5001/docs")
    app.run(debug=True, port=5001)
