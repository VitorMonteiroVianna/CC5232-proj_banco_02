-- Tempo Médio de Conclusão dos Serviços por Especialidade
-- Esta query calcula o tempo médio, em dias, que cada especialidade leva para ter seus serviços concluídos e pagos na plataforma.
-- A consulta cruza dados de especialidades, prestadores, solicitações e pagamentos, considerando apenas serviços concluídos e pagos.
-- Os resultados permitem identificar quais tipos de serviço são realizados mais rapidamente, auxiliando na análise de eficiência operacional por especialidade.

SELECT 
    e.nome AS especialidade,
    ROUND(AVG(p.data_pagamento - s.data_criacao), 1) AS tempo_medio_dias
FROM Especialidade e
JOIN Prestador_especialidade pe ON e.id = pe.id_especialidade
JOIN Solicitacao s ON pe.id_prestador = s.id_prestador
JOIN pagamento p ON s.id = p.id_solicitacao
WHERE s.status = 'Concluído' AND p.status = 'Pago'
GROUP BY e.nome
ORDER BY tempo_medio_dias ASC;