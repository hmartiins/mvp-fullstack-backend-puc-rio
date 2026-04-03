from flask import jsonify

from models import get_db
from utils import row_to_dict
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
        conn = get_db()
        row = conn.execute(
            """
            SELECT d.id, d.descricao, d.valor, d.data, d.categoria_id, c.nome AS categoria_nome
            FROM despesas d
            JOIN categorias c ON c.id = d.categoria_id
            WHERE d.id = ?
            """,
            (despesa_id,),
        ).fetchone()
        conn.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar despesa", "detalhe": str(e)}), 500

    if not row:
        return jsonify({"erro": "Despesa não encontrada"}), 404

    return jsonify(row_to_dict(row)), 200
