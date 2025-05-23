-- Análise Financeira de Pagamentos e Inadimplência
-- Analisa a qualidade dos serviços prestados por região geográfica, utilizando o DDD dos telefones dos prestadores como proxy para localização, identificando padrões regionais de performance e problemas.
--A query extrai o DDD do telefone dos prestadores para agrupá-los por região, calculando métricas de qualidade como taxa de conclusão, taxa de reclamação e média de avaliações. Cruza dados de solicitações, reclamações, evidências e avaliações para fornecer uma visão completa da qualidade regional.

SELECT 
    TO_CHAR(p.data_pagamento, 'MM/YYYY') as mes_ano,
    COUNT(p.id) as total_transacoes,
    COUNT(CASE WHEN p.status = 'Pago' THEN 1 END) as pagamentos_realizados,
    COUNT(CASE WHEN p.status = 'Pendente' THEN 1 END) as pagamentos_pendentes,
    COUNT(CASE WHEN p.status = 'Vencido' THEN 1 END) as pagamentos_vencidos,
    ROUND(SUM(CASE WHEN p.status = 'Pago' THEN p.valor ELSE 0 END), 2) as receita_confirmada,
    ROUND(SUM(CASE WHEN p.status = 'Pendente' THEN p.valor ELSE 0 END), 2) as receita_pendente,
    ROUND(SUM(CASE WHEN p.status = 'Vencido' THEN p.valor ELSE 0 END), 2) as receita_perdida,
    ROUND(
        (COUNT(CASE WHEN p.status = 'Vencido' THEN 1 END)::DECIMAL / COUNT(p.id)) * 100, 
        2
    ) as taxa_inadimplencia_pct,
FROM pagamento p
WHERE p.data_pagamento >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY TO_CHAR(p.data_pagamento, 'MM/YYYY'), DATE_TRUNC('month', p.data_pagamento)
ORDER BY DATE_TRUNC('month', p.data_pagamento) DESC;
