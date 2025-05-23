-- Quantidade de Serviços Realizados por Especialidade
-- Esta query apresenta o total de serviços realizados para cada especialidade cadastrada na plataforma.
-- A consulta cruza dados de especialidades, prestadores e solicitações, permitindo identificar quais áreas possuem maior demanda de serviços.

SELECT 
    e.nome AS especialidade,
    COUNT(s.id) AS total_servicos
FROM Especialidade e
JOIN Prestador_especialidade pe ON e.id = pe.id_especialidade
JOIN Solicitacao s ON pe.id_prestador = s.id_prestador
GROUP BY e.nome
ORDER BY total_servicos DESC;