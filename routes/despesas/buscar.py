from flask import jsonify

from model.models import db, Despesa
from routes.despesas import bp


@bp.route("/<string:despesa_id>", methods=["GET"])
def buscar_despesa(despesa_id):
    """
    Buscar despesa pelo ID
    ---
    tags:
      - Despesas
    parameters:
      - in: path
        name: despesa_id
        type: string
        required: true
        description: UUID da despesa
    responses:
      200:
        description: Despesa encontrada
        schema:
          $ref: '#/definitions/Despesa'
      404:
        description: Despesa não encontrada
        schema:
          $ref: '#/definitions/Erro'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    try:
        despesa = db.session.get(Despesa, despesa_id)
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar despesa", "detalhe": str(e)}), 500

    if not despesa:
        return jsonify({"erro": "Despesa não encontrada"}), 404

    return jsonify(despesa.to_dict()), 200
