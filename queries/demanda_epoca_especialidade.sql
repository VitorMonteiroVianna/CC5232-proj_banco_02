-- Análise de Demanda por Especialidade e Sazonalidade
-- Analisa padrões de demanda por tipo de serviço ao longo do tempo, identificando tendências sazonais e oportunidades de mercado.
-- A query agrupa dados por especialidade e mês, calculando volumes de demanda, faturamento e qualidade do serviço. Utiliza window functions para criar um ranking mensal de demanda, permitindo comparações temporais e identificação de tendências.

SELECT 
    e.nome as especialidade,
    EXTRACT(MONTH FROM s.data_criacao) as mes,
    TO_CHAR(DATE_TRUNC('month', s.data_criacao), 'MM/YYYY') as periodo,
    COUNT(s.id) as total_solicitacoes,
    ROUND(AVG(s.valor), 2) as valor_medio,
    ROUND(SUM(s.valor), 2) as faturamento_total,
    COUNT(CASE WHEN s.status = 'Concluído' THEN 1 END) as servicos_finalizados,
    COUNT(r.id) as reclamacoes_periodo,
    RANK() OVER (
        PARTITION BY EXTRACT(MONTH FROM s.data_criacao) 
        ORDER BY COUNT(s.id) DESC
    ) as ranking_demanda_mensal
FROM Especialidade e
JOIN Prestador_especialidade pe ON e.id = pe.id_especialidade
JOIN Solicitacao s ON pe.id_prestador = s.id_prestador
LEFT JOIN Reclamacao r ON s.id = r.id_solicitacao
WHERE s.data_criacao >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY e.nome, EXTRACT(MONTH FROM s.data_criacao), DATE_TRUNC('month', s.data_criacao)
ORDER BY periodo DESC, total_solicitacoes DESC;
