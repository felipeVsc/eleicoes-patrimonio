SELECT
    CAST(CD_ELEICAO AS INT)                    AS cd_eleicao,
    CAST(ANY_VALUE(ANO_ELEICAO) AS INT)        AS ano_eleicao,
    CAST(ANY_VALUE(CD_TIPO_ELEICAO) AS INT)    AS cd_tipo_eleicao,
    UPPER(ANY_VALUE(NM_TIPO_ELEICAO))          AS nm_tipo_eleicao,
    ANY_VALUE(DS_ELEICAO)                      AS ds_eleicao,
    ANY_VALUE(DT_ELEICAO)                      AS dt_eleicao
FROM {{ ref('silver_candidatos') }}
GROUP BY CAST(CD_ELEICAO AS INT)
