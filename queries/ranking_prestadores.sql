-- Ranking de Prestadores por Desempenho
-- Esta query analisa o desempenho dos prestadores de serviço, fornecendo métricas essenciais para identificar os profissionais mais eficientes e rentáveis da plataforma.
-- A query cruza dados de prestadores, suas especialidades, solicitações de serviço, avaliações e reclamações. Calcula métricas agregadas como receita total, taxa de sucesso e média de avaliações, ordenando os resultados pelos prestadores mais rentáveis e bem avaliados.

SELECT 
    p.nome as prestador,
    e.nome as especialidade,
    COUNT(s.id) as total_servicos,
    ROUND(AVG(s.valor), 2) as ticket_medio,
    ROUND(SUM(s.valor), 2) as receita_total,
    COUNT(CASE WHEN s.status = 'Concluído' THEN 1 END) as servicos_concluidos,
    ROUND(
        (COUNT(CASE WHEN s.status = 'Concluído' THEN 1 END)::DECIMAL / COUNT(s.id)) * 100, 
        2
    ) as taxa_sucesso_pct,
    ROUND(AVG(CAST(a.qtd_estrelas AS DECIMAL)), 2) as media_avaliacoes,
    COUNT(r.id) as total_reclamacoes
FROM Prestador p
JOIN Prestador_especialidade pe ON p.id = pe.id_prestador
JOIN Especialidade e ON pe.id_especialidade = e.id
LEFT JOIN Solicitacao s ON p.id = s.id_prestador
LEFT JOIN Avalicao a ON p.id = a.id_prestador
LEFT JOIN Reclamacao r ON s.id = r.id_solicitacao
GROUP BY p.id, p.nome, e.nome
HAVING COUNT(s.id) > 0
ORDER BY receita_total DESC, media_avaliacoes DESC
LIMIT 10;
