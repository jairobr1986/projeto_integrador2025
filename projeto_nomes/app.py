from flask import Flask, render_template, request, redirect, send_file
from db import init_db, get_connection
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

# ============================
# Inicializa o banco
# ============================
init_db()

# ============================
# Rota principal (home)
# ============================
@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM nomes")
    total = cursor.fetchone()[0]

    # Top 10 nomes mais pesquisados
    cursor.execute("SELECT nome, pesquisas FROM nomes ORDER BY pesquisas DESC LIMIT 10")
    top_nomes = cursor.fetchall()
    conn.close()

    return render_template("index.html", total=total, top_nomes=top_nomes)

# ============================
# Cadastrar nomes
# ============================
@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        significado = request.form["significado"].strip()
        origem = request.form["origem"].strip()
        motivo = request.form["motivo"].strip()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nomes (nome, significado, origem, motivo_escolha)
            VALUES (?, ?, ?, ?)
        """, (nome, significado, origem, motivo))
        conn.commit()
        conn.close()
        return redirect("/")
    return render_template("cadastrar.html")

# ============================
# Listar nomes com filtros e paginação
# ============================
@app.route("/listar")
def listar():
    page = int(request.args.get("page", 1))
    per_page = 77
    filtro_nome = request.args.get("nome", "").strip()
    filtro_origem = request.args.get("origem", "").strip()

    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM nomes WHERE 1=1"
    params = []

    if filtro_nome:
        query += " AND nome LIKE ?"
        params.append("%" + filtro_nome + "%")
    if filtro_origem:
        query += " AND origem LIKE ?"
        params.append("%" + filtro_origem + "%")

    cursor.execute(query.replace("*", "COUNT(*)"), params)
    total = cursor.fetchone()[0]

    offset = (page - 1) * per_page
    query += " LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    cursor.execute(query, params)
    nomes = cursor.fetchall()
    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template("listar.html",
                           nomes=nomes,
                           page=page,
                           total_pages=total_pages,
                           filtro_nome=filtro_nome,
                           filtro_origem=filtro_origem)

# ============================
# Buscar nomes e incrementar pesquisas
# ============================
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    resultados = []
    termo = ""

    if request.method == "POST":
        termo = request.form["termo"].strip().lower()
    else:
        termo = request.args.get("termo", "").strip().lower()

    if termo:
        conn = get_connection()
        cursor = conn.cursor()

        # Busca case-insensitive
        cursor.execute("SELECT * FROM nomes WHERE LOWER(nome) LIKE ?", ('%' + termo + '%',))
        resultados = cursor.fetchall()

        # Incrementa contador de pesquisas
        for row in resultados:
            cursor.execute("UPDATE nomes SET pesquisas = pesquisas + 1 WHERE id = ?", (row[0],))
        conn.commit()
        conn.close()

    return render_template("buscar.html", resultados=resultados, termo=termo)

# ============================
# Estatísticas e gráficos
# ============================
@app.route("/estatisticas")
def estatisticas():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM nomes", conn)
    conn.close()

    if df.empty:
        return render_template("estatisticas.html",
                               total=0,
                               mais_comum="Nenhum",
                               origem_comum="Nenhuma")

    total = len(df)
    mais_comum = df["nome"].mode()[0]
    origem_comum = df["origem"].mode()[0] if df["origem"].notna().any() else "Nenhuma"

    # Gráfico 1: Top 5 nomes
    plt.figure(figsize=(6,4))
    df["nome"].value_counts().head(5).plot(kind="bar", color="skyblue")
    plt.title("Top 5 Nomes Mais Comuns")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.savefig("static/nomes_comuns.png")
    plt.close()

    # Gráfico 2: Origem
    plt.figure(figsize=(5,5))
    df["origem"].value_counts().plot(kind="pie", autopct="%1.1f%%")
    plt.title("Distribuição das Origens")
    plt.tight_layout()
    plt.savefig("static/origens.png")
    plt.close()

    return render_template("estatisticas.html",
                           total=total,
                           mais_comum=mais_comum,
                           origem_comum=origem_comum)

# ============================
# Exportar CSV
# ============================
@app.route("/exportar")
def exportar():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM nomes", conn)
    conn.close()

    buffer = BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="nomes_exportados.csv", mimetype="text/csv")

# ============================
# Top 10 nomes mais pesquisados
# ============================
@app.route("/top10")
def top10():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, pesquisas FROM nomes ORDER BY pesquisas DESC LIMIT 10")
    top_nomes = cursor.fetchall()
    conn.close()
    return render_template("top10.html", top_nomes=top_nomes)

# ============================
# Executar app
# ============================
if __name__ == "__main__":
    app.run(debug=True)
