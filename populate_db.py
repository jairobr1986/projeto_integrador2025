import sqlite3
from db import init_db, get_connection

# Inicializa a tabela (caso ainda não exista)
init_db()

# Lista de nomes de exemplo
nomes = [
    ("Alice", "Nobre", "Hebraica", "Escolhido pelos pais por tradição"),
    ("Bruno", "Castanho, moreno", "Germânica", "Gostaram do som do nome"),
    ("Clara", "Brilhante, clara", "Latina", "Significado positivo"),
    ("Daniel", "Deus é meu juiz", "Hebraica", "Homenagem a um parente"),
    
]

# Conecta ao banco
conn = get_connection()
cursor = conn.cursor()

# Insere os nomes no banco
for nome, significado, origem, motivo in nomes:
    # Verifica se o nome já existe para não duplicar
    cursor.execute("SELECT id FROM nomes WHERE nome = ?", (nome,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO nomes (nome, significado, origem, motivo_escolha, pesquisas)
            VALUES (?, ?, ?, ?, 0)
        """, (nome, significado, origem, motivo))

conn.commit()
conn.close()

print("Banco populado com sucesso!")
