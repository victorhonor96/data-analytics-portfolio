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
SELECT * FROM base;