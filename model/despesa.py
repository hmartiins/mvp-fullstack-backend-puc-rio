from model.database import db


class Despesa(db.Model):
    __tablename__ = "despesas"

    id = db.Column(db.String, primary_key=True)
    descricao = db.Column(db.String, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.Date, nullable=False)
    categoria_id = db.Column(db.String, db.ForeignKey("categorias.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "valor": self.valor,
            "data": self.data.isoformat() if self.data else None,
            "categoria_id": self.categoria_id,
            "categoria_nome": self.categoria.nome if self.categoria else None,
        }
