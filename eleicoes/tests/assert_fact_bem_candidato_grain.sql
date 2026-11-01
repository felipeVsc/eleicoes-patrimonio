-- grain of gold_fact_bem_candidato: one row per (sq_candidato, nr_ordem_bem)
SELECT
    sq_candidato,
    nr_ordem_bem,
    COUNT(*) AS qt
FROM {{ ref('gold_fact_bem_candidato') }}
GROUP BY sq_candidato, nr_ordem_bem
HAVING COUNT(*) > 1
