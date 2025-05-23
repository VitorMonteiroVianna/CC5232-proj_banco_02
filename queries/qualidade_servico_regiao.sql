-- Análise de Qualidade de Serviço por Região (DDD)
-- Analisa a qualidade dos serviços prestados por região geográfica, utilizando o DDD dos telefones dos prestadores como proxy para localização, identificando padrões regionais de performance e problemas.
--A query extrai o DDD do telefone dos prestadores para agrupá-los por região, calculando métricas de qualidade como taxa de conclusão, taxa de reclamação e média de avaliações. Cruza dados de solicitações, reclamações, evidências e avaliações para fornecer uma visão completa da qualidade regional.

SELECT 
    SUBSTRING(p.telefone, 2, 2) as ddd_regiao,
    COUNT(DISTINCT p.id) as total_prestadores,
    COUNT(s.id) as total_servicos,
    ROUND(AVG(s.valor), 2) as ticket_medio_regiao,
    COUNT(CASE WHEN s.status = 'Concluído' THEN 1 END) as servicos_concluidos,
    ROUND(
        (COUNT(CASE WHEN s.status = 'Concluído' THEN 1 END)::DECIMAL / COUNT(s.id)) * 100, 
        2
    ) as taxa_conclusao_pct,
    COUNT(r.id) as total_reclamacoes,
    ROUND(
        (COUNT(r.id)::DECIMAL / NULLIF(COUNT(s.id), 0)) * 100, 
        2
    ) as taxa_reclamacao_pct,
    ROUND(AVG(CAST(a.qtd_estrelas AS DECIMAL)), 2) as media_avaliacoes_regiao,
    COUNT(e.id) as evidencias_problemas
FROM Prestador p
LEFT JOIN Solicitacao s ON p.id = s.id_prestador
LEFT JOIN Reclamacao r ON s.id = r.id_solicitacao
LEFT JOIN evidencia e ON r.id = e.id_reclamacao
LEFT JOIN Avalicao a ON p.id = a.id_prestador
GROUP BY SUBSTRING(p.telefone, 2, 2)
HAVING COUNT(s.id) > 0
ORDER BY taxa_reclamacao_pct ASC, media_avaliacoes_regiao DESC;
