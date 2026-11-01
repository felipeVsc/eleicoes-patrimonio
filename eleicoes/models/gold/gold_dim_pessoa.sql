-- One row per person. Attributes that can change between candidacies
-- (name, race, gender, ...) live in gold_dim_candidatura, so different
-- candidacies of the same person can be compared through sk_pessoa.
WITH candidatos AS (
    SELECT
        *,
        {{ sk_pessoa() }} AS sk_pessoa
    FROM {{ ref('silver_candidatos') }}
)

SELECT
    sk_pessoa,
    CASE
        WHEN regexp_full_match(ANY_VALUE(NR_CPF_CANDIDATO), '[0-9]{11}')
            THEN ANY_VALUE(NR_CPF_CANDIDATO)
    END                                         AS nr_cpf,
    COUNT(*)                                    AS qt_candidaturas,
    CAST(MIN(ANO_ELEICAO) AS INT)               AS ano_primeira_candidatura,
    CAST(MAX(ANO_ELEICAO) AS INT)               AS ano_ultima_candidatura
FROM candidatos
GROUP BY sk_pessoa
