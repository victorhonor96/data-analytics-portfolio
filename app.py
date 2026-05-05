import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Data Analytics Portfolio", layout="wide")

conn = sqlite3.connect("database.db")

def query(sql):
    return pd.read_sql_query(sql, conn)

st.title("📊 Data Analytics Dashboard")

menu = st.sidebar.selectbox("Escolha:", ["Obras", "Educacional", "Preços"])

# =========================
# 🏗️ OBRAS
# =========================
if menu == "Obras":
    st.header("🏗️ Análise de Obras")

    sql = """
    WITH base AS (
        SELECT *,
               (custo_real - custo_previsto) AS desvio,
               CASE 
                   WHEN custo_real > custo_previsto AND status = 'Atrasada' THEN 'Crítica'
                   WHEN custo_real > custo_previsto THEN 'Financeiro'
                   WHEN status = 'Atrasada' THEN 'Prazo'
                   ELSE 'OK'
               END AS risco
        FROM obras
    )
    SELECT * FROM base
    """

    df = query(sql)

    col1, col2, col3 = st.columns(3)
    col1.metric("Custo Total", f"R$ {df['custo_real'].sum():,.0f}")
    col2.metric("Desvio Total", f"R$ {df['desvio'].sum():,.0f}")
    col3.metric("Obras Críticas", (df["risco"] == "Crítica").sum())

    fig = px.bar(df, x="fornecedor", y="custo_real", title="Custo por Fornecedor")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Obras Críticas")
    st.dataframe(df[df["risco"] == "Crítica"])

    with st.expander("Ver SQL"):
        st.code(sql, language="sql")

# =========================
# 🎓 EDUCACIONAL
# =========================
elif menu == "Educacional":
    st.header("🎓 Análise Educacional")

    sql = """
    SELECT 
        a.nome,
        n.disciplina,
        AVG(n.nota) AS media,
        AVG(n.frequencia) AS freq
    FROM alunos a
    JOIN notas n ON a.id_aluno = n.id_aluno
    GROUP BY a.nome, n.disciplina
    """

    df = query(sql)

    st.metric("Média Geral", round(df["media"].mean(), 2))

    fig = px.bar(df, x="disciplina", y="media", color="disciplina")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Ver SQL"):
        st.code(sql, language="sql")

# =========================
# 💰 PREÇOS
# =========================
elif menu == "Preços":
    st.header("💰 Análise de Preços")

    sql = """
    SELECT *
    FROM (
        SELECT 
            p.nome_produto,
            pr.fornecedor,
            pr.preco,
            ROW_NUMBER() OVER (
                PARTITION BY p.id_produto 
                ORDER BY pr.preco ASC
            ) AS rn
        FROM produtos p
        JOIN precos pr ON p.id_produto = pr.id_produto
    )
    WHERE rn = 1
    """

    df = query(sql)

    st.metric("Melhor Preço Médio", round(df["preco"].mean(), 2))

    fig = px.bar(df, x="nome_produto", y="preco", color="fornecedor")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Ver SQL"):
        st.code(sql, language="sql")