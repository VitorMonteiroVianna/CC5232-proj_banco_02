-- Ranking de Prestadores com Mais Reclamações
-- Esta query identifica os prestadores que mais receberam reclamações na plataforma, permitindo analisar possíveis problemas de atendimento ou qualidade de serviço.
-- A consulta cruza dados de prestadores, solicitações, reclamações e avaliações, trazendo o total de reclamações e a média das avaliações para cada prestador.
-- Esses resultdos são ordenados para destacar os profissionais com maior numero de reclamações e avaliações mais baixas, facilitanado a identificação de casos problematiocos

SELECT 
    p.nome AS prestador,
    COUNT(r.id) AS total_reclamacoes,
    ROUND(AVG(CAST(a.qtd_estrelas AS DECIMAL)), 2) AS media_avaliacoes
FROM Prestador p
LEFT JOIN Solicitacao s ON p.id = s.id_prestador
LEFT JOIN Reclamacao r ON s.id = r.id_solicitacao
LEFT JOIN Avalicao a ON p.id = a.id_prestador
GROUP BY p.id, p.nome
HAVING COUNT(r.id) > 0
ORDER BY total_reclamacoes DESC, media_avaliacoes ASC
LIMIT 10;

