from flask import jsonify

from model.models import get_db
from utils import row_to_dict
from routes.despesas import bp


@bp.route("/resumo", methods=["GET"])
def resumo_despesas():
    """
    Total gasto agrupado por categoria
    ---
    tags:
      - Despesas
    responses:
      200:
        description: Resumo com total e quantidade de despesas por categoria
        schema:
          type: array
          items:
            $ref: '#/definitions/Resumo'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    try:
        conn = get_db()
        rows = conn.execute(
            """
            SELECT c.id AS categoria_id, c.nome AS categoria_nome,
                   ROUND(SUM(d.valor), 2) AS total,
                   COUNT(d.id) AS quantidade
            FROM categorias c
            LEFT JOIN despesas d ON d.categoria_id = c.id
            GROUP BY c.id, c.nome
            ORDER BY total DESC
            """
        ).fetchall()
        conn.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao gerar resumo", "detalhe": str(e)}), 500

    return jsonify([row_to_dict(r) for r in rows]), 200
