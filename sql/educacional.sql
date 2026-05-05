SELECT 
    a.nome,
    n.disciplina,
    AVG(n.nota) AS media,
    AVG(n.frequencia) AS freq
FROM alunos a
JOIN notas n ON a.id_aluno = n.id_aluno
GROUP BY a.nome, n.disciplina;