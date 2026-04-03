from flask import jsonify

from model.models import db, Categoria, Despesa
from schemas.categoria import CategoriaPath
from schemas.comum import ErroResponse, MensagemResponse
from routes.categorias import bp


@bp.delete(
    "/<categoria_id>",
    responses={"200": MensagemResponse, "404": ErroResponse, "409": ErroResponse},
)
def deletar_categoria(path: CategoriaPath):
    """Deletar uma categoria pelo ID"""
    categoria_id = path.categoria_id

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
