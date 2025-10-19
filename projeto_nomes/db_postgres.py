import psycopg2
from psycopg2 import sql

# =================================================================
# ATENÇÃO: COLOQUE SUA SENHA FORTE AQUI!
# Os outros valores foram extraídos da sua URL de conexão do Supabase.
# =================================================================
DB_CONFIG = {
    "host": "db.cgrxdexfgqnyguteaobu.supabase.co", 
    "database": "postgres", 
    "user": "postgres",     
    "password": "projeto_integrador_2025_banco_de_dados", # <-- SUBSTITUA ESTE VALOR
    "port": "5432" 
}
# =================================================================

def get_connection():
    """Retorna uma nova conexão com o banco de dados PostgreSQL na nuvem."""
    try:
        # Tenta conectar usando as configurações fornecidas
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao PostgreSQL: {e}")
        # É crucial que o app falhe se não puder conectar ao DB
        raise e

def init_db():
    """Inicializa o banco de dados, criando a tabela 'nomes' se ela não existir."""
    conn = None # Inicializa conn para garantir que existe no finally
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # O SERIAL PRIMARY KEY garante o auto-incremento no PostgreSQL
        create_table_query = """
            CREATE TABLE IF NOT EXISTS nomes (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                significado TEXT,
                origem VARCHAR(100),
                motivo_escolha TEXT,
                pesquisas INTEGER DEFAULT 0
            );
        """
        cursor.execute(create_table_query)
        conn.commit()
        print("Tabela 'nomes' verificada/criada no PostgreSQL na nuvem com sucesso.")
        
    except psycopg2.Error as e:
        print(f"Erro durante a inicialização do DB: {e}")
        
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Execute este arquivo uma vez para criar a tabela no seu DB na nuvem
    init_db()
