from flask import jsonify

from model.models import db, Categoria, Despesa
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
        categoria = db.session.get(Categoria, categoria_id)
        if not categoria:
            return jsonify({"erro": "Categoria não encontrada"}), 404

        vinculadas = Despesa.query.filter_by(categoria_id=categoria_id).count()
        if vinculadas > 0:
            return jsonify(
                {"erro": f"Não é possível deletar: categoria possui {vinculadas} despesa(s) vinculada(s)"}
            ), 409

        db.session.delete(categoria)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar categoria", "detalhe": str(e)}), 500

    return jsonify({"mensagem": f"Categoria {categoria_id} deletada com sucesso"}), 200
