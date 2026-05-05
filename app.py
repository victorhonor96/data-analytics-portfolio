import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Dashboard", layout="wide")

st.title("📊 Data Analytics Dashboard")

# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    obras = pd.read_csv("data/obras.csv")
    alunos = pd.read_csv("data/alunos.csv")
    notas = pd.read_csv("data/notas.csv")
    produtos = pd.read_csv("data/produtos.csv")
    precos = pd.read_csv("data/precos.csv")
    return obras, alunos, notas, produtos, precos

obras, alunos, notas, produtos, precos = load_data()

# ======================
# MENU
# ======================
aba = st.sidebar.selectbox(
    "Escolha a análise:",
    ["Obras", "Educacional", "Preços"]
)

# ======================
# 🏗️ OBRAS
# ======================
if aba == "Obras":
    st.header("🏗️ Análise de Obras")

    obras["desvio"] = obras["custo_real"] - obras["custo_previsto"]

    col1, col2, col3 = st.columns(3)

    col1.metric("Custo Total", f"R$ {obras['custo_real'].sum():,.0f}")
    col2.metric("Desvio Total", f"R$ {obras['desvio'].sum():,.0f}")
    col3.metric("Obras Atrasadas", obras["status"].str.contains("Atrasada").sum())

    fig = px.bar(obras, x="fornecedor", y="custo_real", title="Custo por Fornecedor")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(obras, x="nome_obra", y=["custo_previsto", "custo_real"],
                  barmode="group", title="Previsto vs Real")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Obras Críticas")
    criticas = obras[(obras["custo_real"] > obras["custo_previsto"]) &
                     (obras["status"] == "Atrasada")]
    st.dataframe(criticas)

# ======================
# 🎓 EDUCACIONAL
# ======================
elif aba == "Educacional":
    st.header("🎓 Análise Educacional")

    df = notas.merge(alunos, on="id_aluno")

    col1, col2 = st.columns(2)

    col1.metric("Média Geral", round(df["nota"].mean(), 2))
    col2.metric("Taxa Aprovação", f"{(df['nota'] >= 6).mean()*100:.1f}%")

    fig = px.bar(df, x="disciplina", y="nota", color="disciplina",
                 title="Notas por Disciplina", barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.scatter(df, x="frequencia", y="nota",
                      title="Frequência vs Nota")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Alunos em risco")
    risco = df[(df["nota"] < 6) | (df["frequencia"] < 75)]
    st.dataframe(risco)

# ======================
# 💰 PREÇOS
# ======================
elif aba == "Preços":
    st.header("💰 Análise de Preços")

    df = precos.merge(produtos, on="id_produto")

    col1, col2 = st.columns(2)

    col1.metric("Preço Médio", round(df["preco"].mean(), 2))
    col2.metric("Menor Preço", round(df["preco"].min(), 2))

    fig = px.bar(df, x="nome_produto", y="preco", color="fornecedor",
                 title="Comparação de Preços")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Tabela Comparativa")
    st.dataframe(df)