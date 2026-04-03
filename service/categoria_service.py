import uuid
from typing import Optional, List

from sqlalchemy.exc import IntegrityError

from model import db, Categoria, Despesa
from service.exceptions import NotFoundError, ConflictError


def criar(nome: str, descricao: Optional[str]) -> Categoria:
    try:
        categoria = Categoria(id=str(uuid.uuid4()), nome=nome, descricao=descricao)
        db.session.add(categoria)
        db.session.commit()
        return categoria
    except IntegrityError:
        db.session.rollback()
        raise ConflictError(f"Já existe uma categoria com o nome '{nome}'")


def listar() -> List[Categoria]:
    return Categoria.query.order_by(Categoria.nome).all()


def deletar(categoria_id: str) -> None:
    categoria = db.session.get(Categoria, categoria_id)
    if not categoria:
        raise NotFoundError("Categoria não encontrada")

    vinculadas = Despesa.query.filter_by(categoria_id=categoria_id).count()
    if vinculadas > 0:
        raise ConflictError(
            f"Não é possível deletar: categoria possui {vinculadas} despesa(s) vinculada(s)"
        )

    db.session.delete(categoria)
    db.session.commit()
