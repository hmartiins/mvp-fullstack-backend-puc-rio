from flask import jsonify

from model.models import Categoria
from schemas.categoria import CategoriaResponse
from schemas.comum import ErroResponse
from routes.categorias import bp


@bp.get("", responses={"200": CategoriaResponse, "500": ErroResponse})
def listar_categorias():
    """Listar todas as categorias"""
    try:
        categorias = Categoria.query.order_by(Categoria.nome).all()
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar categorias", "detalhe": str(e)}), 500

    return jsonify([c.to_dict() for c in categorias]), 200
