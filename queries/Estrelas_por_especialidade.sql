-- Serviços de Tapeçaria e Marcenaria: Distribuição de Avaliações
-- Esta query retorna a quantidade de serviços realizados nas especialidades 'Tapeçaria' e 'Marcenaria',
-- mostrando quantos desses serviços receberam 5, 4, 3, 2 e 1 estrela em suas avaliações.

SELECT 
    e.nome AS especialidade,
    a.qtd_estrelas,
    COUNT(*) AS quantidade_servicos
FROM Especialidade e
JOIN Prestador_especialidade pe ON e.id = pe.id_especialidade
JOIN Solicitacao s ON pe.id_prestador = s.id_prestador
JOIN Avalicao a ON s.id_prestador = a.id_prestador
WHERE e.id IN (31, 39)
GROUP BY e.nome, a.qtd_estrelas
ORDER BY e.nome, a.qtd_estrelas DESC;