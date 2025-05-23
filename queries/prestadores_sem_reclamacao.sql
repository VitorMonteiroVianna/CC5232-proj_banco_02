-- Prestadores sem Reclamações +qtd Estrelas
-- Esta query destaca os prestadores que nunca receberam reclamações, evidenciando profissionais com histórico de atendimento exemplar.
-- A consulta reúne informações de prestadores, solicitações, reclamações e avaliações, mostrando a média das avaliações dos prestadores sem nenhuma reclamação registrada.
-- Os resultados ajudam a reconhecer e valorizar os profissionais mais bem avaliados e confiáveis da plataforma.

SELECT 
    p.nome AS prestador,
    ROUND(AVG(CAST(a.qtd_estrelas AS DECIMAL)), 2) AS media_avaliacoes,
    COUNT(s.id) AS total_servicos
FROM Prestador p
LEFT JOIN Solicitacao s ON p.id = s.id_prestador
LEFT JOIN Avalicao a ON p.id = a.id_prestador
LEFT JOIN Reclamacao r ON s.id = r.id_solicitacao
GROUP BY p.id, p.nome
HAVING COUNT(r.id) = 0 AND AVG(CAST(a.qtd_estrelas AS DECIMAL)) >= 4
ORDER BY media_avaliacoes DESC, total_servicos DESC
LIMIT 10;

