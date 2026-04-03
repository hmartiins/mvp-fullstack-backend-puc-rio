from flask import jsonify

from model.models import Despesa
from routes.despesas import bp


@bp.route("", methods=["GET"])
def listar_despesas():
    """
    Listar todas as despesas
    ---
    tags:
      - Despesas
    responses:
      200:
        description: Lista de despesas com nome da categoria
        schema:
          type: array
          items:
            $ref: '#/definitions/Despesa'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    try:
        despesas = Despesa.query.order_by(Despesa.data.desc(), Despesa.id.desc()).all()
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar despesas", "detalhe": str(e)}), 500

    return jsonify([d.to_dict() for d in despesas]), 200
