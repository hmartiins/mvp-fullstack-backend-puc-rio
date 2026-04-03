from flask import jsonify

from model.models import Categoria
from routes.categorias import bp


@bp.route("", methods=["GET"])
def listar_categorias():
    """
    Listar todas as categorias
    ---
    tags:
      - Categorias
    responses:
      200:
        description: Lista de categorias
        schema:
          type: array
          items:
            $ref: '#/definitions/Categoria'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    try:
        categorias = Categoria.query.order_by(Categoria.nome).all()
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar categorias", "detalhe": str(e)}), 500

    return jsonify([c.to_dict() for c in categorias]), 200
