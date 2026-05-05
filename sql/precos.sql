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
WHERE rn = 1;