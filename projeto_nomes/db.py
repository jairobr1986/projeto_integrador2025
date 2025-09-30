import sqlite3

def get_connection():
    """Retorna uma conexão com o banco de dados."""
    return sqlite3.connect("nomes.db")

def init_db():
    """Cria a tabela 'nomes' se não existir, incluindo contador de pesquisas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            significado TEXT,
            origem TEXT,
            motivo_escolha TEXT,
            pesquisas INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
