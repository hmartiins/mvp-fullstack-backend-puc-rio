from flask import jsonify

from models import get_db
from routes.despesas import bp


@bp.route("/<string:despesa_id>", methods=["DELETE"])
def deletar_despesa(despesa_id):
    """
    Deletar uma despesa pelo ID
    ---
    tags:
      - Despesas
    parameters:
      - in: path
        name: despesa_id
        type: string
        required: true
        description: UUID da despesa a deletar
    responses:
      200:
        description: Despesa deletada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
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
        conn = get_db()

        despesa = conn.execute(
            "SELECT id FROM despesas WHERE id = ?", (despesa_id,)
        ).fetchone()
        if not despesa:
            conn.close()
            return jsonify({"erro": "Despesa não encontrada"}), 404

        conn.execute("DELETE FROM despesas WHERE id = ?", (despesa_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao deletar despesa", "detalhe": str(e)}), 500

    return jsonify({"mensagem": f"Despesa {despesa_id} deletada com sucesso"}), 200
