import sqlite3

DATABASE = "gastos.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id          TEXT PRIMARY KEY,
            nome        TEXT NOT NULL UNIQUE,
            descricao   TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS despesas (
            id           TEXT PRIMARY KEY,
            descricao    TEXT NOT NULL,
            valor        REAL NOT NULL,
            data         TEXT NOT NULL,
            categoria_id TEXT NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    """
    )

    conn.commit()
    conn.close()
