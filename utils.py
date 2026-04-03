from datetime import datetime


def parse_date(value: str):
    """Valida e retorna a data no formato YYYY-MM-DD ou lança ValueError."""
    return datetime.strptime(value, "%Y-%m-%d").date()


def row_to_dict(row) -> dict:
    return dict(row) if row else None
