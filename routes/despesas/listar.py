from flask import jsonify

from models import get_db
from utils import row_to_dict
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
        conn = get_db()
        rows = conn.execute(
            """
            SELECT d.id, d.descricao, d.valor, d.data, d.categoria_id, c.nome AS categoria_nome
            FROM despesas d
            JOIN categorias c ON c.id = d.categoria_id
            ORDER BY d.data DESC, d.id DESC
            """
        ).fetchall()
        conn.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao buscar despesas", "detalhe": str(e)}), 500

    return jsonify([row_to_dict(r) for r in rows]), 200
