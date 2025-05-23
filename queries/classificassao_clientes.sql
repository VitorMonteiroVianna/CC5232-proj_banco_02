-- Perfil de Clientes e Padrões de Consumo (CORRIGIDA)
-- Segmenta clientes baseado em seu comportamento de consumo, histórico de avaliações e padrões de uso da plataforma, permitindo estratégias personalizadas de relacionamento.
-- A query consolida o histórico completo de cada cliente, calculando métricas de consumo, satisfação e engajamento. Aplica regras de negócio para classificar automaticamente os clientes em perfis distintos, facilitando a segmentação para ações de marketing e relacionamento.

SELECT 
    c.nome as cliente,
    COUNT(s.id) as total_servicos_contratados,
    ROUND(SUM(s.valor), 2) as valor_total_gasto,
    ROUND(AVG(s.valor), 2) as ticket_medio,
    COUNT(DISTINCT s.id_prestador) as prestadores_diferentes,
    ROUND(AVG(CAST(a.qtd_estrelas AS DECIMAL)), 2) as media_avaliacoes_dadas,
    COUNT(r.id) as reclamacoes_feitas,
    MAX(s.data_criacao) as ultima_contratacao,
    (CURRENT_DATE - MAX(s.data_criacao)) as dias_sem_contratar,
    CASE 
        WHEN COUNT(s.id) >= 5 AND AVG(CAST(a.qtd_estrelas AS DECIMAL)) >= 4 THEN 'Cliente Premium'
        WHEN COUNT(s.id) >= 3 THEN 'Cliente Frequente'
        WHEN COUNT(r.id) > 1 THEN 'Cliente Problemático'
        WHEN (CURRENT_DATE - MAX(s.data_criacao)) > 90 THEN 'Cliente Inativo'
        ELSE 'Cliente Regular'
    END as perfil_cliente
FROM Cliente c
LEFT JOIN Solicitacao s ON c.id = s.id_cliente
LEFT JOIN Avalicao a ON c.id = a.id_cliente
LEFT JOIN Reclamacao r ON s.id = r.id_solicitacao
GROUP BY c.id, c.nome
HAVING COUNT(s.id) > 0
ORDER BY valor_total_gasto DESC, total_servicos_contratados DESC;
