from flask import jsonify

from model.models import get_db
from routes.categorias import bp


@bp.route("/<string:categoria_id>", methods=["DELETE"])
def deletar_categoria(categoria_id):
    """
    Deletar uma categoria pelo ID
    ---
    tags:
      - Categorias
    parameters:
      - in: path
        name: categoria_id
        type: string
        required: true
        description: UUID da categoria a deletar
    responses:
      200:
        description: Categoria deletada com sucesso
        schema:
          type: object
          properties:
            mensagem:
              type: string
      404:
        description: Categoria não encontrada
        schema:
          $ref: '#/definitions/Erro'
      409:
        description: Categoria possui despesas vinculadas
        schema:
          $ref: '#/definitions/Erro'
      500:
        description: Erro interno
        schema:
          $ref: '#/definitions/Erro'
    """
    try:
        conn = get_db()

        categoria = conn.execute(
            "SELECT id FROM categorias WHERE id = ?", (categoria_id,)
        ).fetchone()
        if not categoria:
            conn.close()
            return jsonify({"erro": "Categoria não encontrada"}), 404

        vinculadas = conn.execute(
            "SELECT COUNT(*) AS qtd FROM despesas WHERE categoria_id = ?", (categoria_id,)
        ).fetchone()["qtd"]
        if vinculadas > 0:
            conn.close()
            return jsonify(
                {"erro": f"Não é possível deletar: categoria possui {vinculadas} despesa(s) vinculada(s)"}
            ), 409

        conn.execute("DELETE FROM categorias WHERE id = ?", (categoria_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"erro": "Erro ao deletar categoria", "detalhe": str(e)}), 500

    return jsonify({"mensagem": f"Categoria {categoria_id} deletada com sucesso"}), 200
