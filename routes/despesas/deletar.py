from flask import jsonify

from model.models import db, Despesa
from schemas.despesa import DespesaPath
from schemas.comum import ErroResponse, MensagemResponse
from routes.despesas import bp


@bp.delete("/<despesa_id>", responses={"200": MensagemResponse, "404": ErroResponse})
def deletar_despesa(path: DespesaPath):
    """Deletar uma despesa pelo ID"""
    try:
        despesa = db.session.get(Despesa, path.despesa_id)
        if not despesa:
            return jsonify({"erro": "Despesa não encontrada"}), 404

        db.session.delete(despesa)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao deletar despesa", "detalhe": str(e)}), 500

    return jsonify({"mensagem": f"Despesa {path.despesa_id} deletada com sucesso"}), 200
