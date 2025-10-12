import os
import sqlite3

# Caminho absoluto do banco de dados (evita criar outro .db em local errado)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "nomes.db")

def get_connection():
    """Retorna uma conexão com o banco de dados."""
    conn = sqlite3.connect(DATABASE, timeout=10)
    conn.row_factory = sqlite3.Row  # permite acessar colunas pelo nome
    return conn

def init_db():
    """Cria a tabela 'nomes' se não existir, incluindo contador de pesquisas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")  # melhora o desempenho

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

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_nome ON nomes(nome)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_origem ON nomes(origem)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("Banco de dados usado:", DATABASE)
