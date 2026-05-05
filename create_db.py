import sqlite3
import pandas as pd

conn = sqlite3.connect("database.db")

obras = pd.read_csv("data/obras.csv")
alunos = pd.read_csv("data/alunos.csv")
notas = pd.read_csv("data/notas.csv")
produtos = pd.read_csv("data/produtos.csv")
precos = pd.read_csv("data/precos.csv")

obras.to_sql("obras", conn, if_exists="replace", index=False)
alunos.to_sql("alunos", conn, if_exists="replace", index=False)
notas.to_sql("notas", conn, if_exists="replace", index=False)
produtos.to_sql("produtos", conn, if_exists="replace", index=False)
precos.to_sql("precos", conn, if_exists="replace", index=False)

conn.close()

print("Banco criado com sucesso!")