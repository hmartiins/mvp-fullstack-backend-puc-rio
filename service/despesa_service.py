import uuid
from datetime import date
from typing import List

from sqlalchemy import func

from model import db, Categoria, Despesa
from service.exceptions import NotFoundError, ConflictError


def criar(descricao: str, valor: float, data: date, categoria_id: str) -> Despesa:
    if not db.session.get(Categoria, categoria_id):
        raise NotFoundError(f"Categoria com id {categoria_id} não encontrada")

    despesa = Despesa(
        id=str(uuid.uuid4()),
        descricao=descricao,
        valor=valor,
        data=data,
        categoria_id=categoria_id,
    )
    db.session.add(despesa)
    db.session.commit()
    return despesa


def listar() -> List[Despesa]:
    return Despesa.query.order_by(Despesa.data.desc(), Despesa.id.desc()).all()


def buscar(despesa_id: str) -> Despesa:
    despesa = db.session.get(Despesa, despesa_id)
    if not despesa:
        raise NotFoundError("Despesa não encontrada")
    return despesa


def deletar(despesa_id: str) -> None:
    despesa = buscar(despesa_id)
    db.session.delete(despesa)
    db.session.commit()


def resumo() -> List[dict]:
    rows = (
        db.session.query(
            Categoria.id.label("categoria_id"),
            Categoria.nome.label("categoria_nome"),
            func.round(func.coalesce(func.sum(Despesa.valor), 0), 2).label("total"),
            func.count(Despesa.id).label("quantidade"),
        )
        .outerjoin(Despesa, Despesa.categoria_id == Categoria.id)
        .group_by(Categoria.id, Categoria.nome)
        .order_by(func.sum(Despesa.valor).desc())
        .all()
    )
    return [
        {
            "categoria_id": r.categoria_id,
            "categoria_nome": r.categoria_nome,
            "total": r.total,
            "quantidade": r.quantidade,
        }
        for r in rows
    ]


def por_periodo(data_inicio: date, data_fim: date) -> List[Despesa]:
    if data_inicio > data_fim:
        raise ConflictError("'data_inicio' não pode ser posterior a 'data_fim'")

    return (
        Despesa.query
        .filter(Despesa.data.between(data_inicio, data_fim))
        .order_by(Despesa.data.asc())
        .all()
    )
