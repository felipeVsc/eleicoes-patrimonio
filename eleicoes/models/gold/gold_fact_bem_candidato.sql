SELECT
    b.CD_ELEICAO                    AS cd_eleicao,
    b.SQ_CANDIDATO                  AS sq_candidato,
    c.sk_pessoa,
    b.CD_TIPO_BEM_CANDIDATO         AS cd_tipo_bem,
    b.ANO_ELEICAO                   AS ano_eleicao,
    b.NR_ORDEM_BEM_CANDIDATO        AS nr_ordem_bem,
    b.DS_BEM_CANDIDATO              AS ds_bem,
    b.VR_BEM_CANDIDATO              AS vr_bem,
    b.DT_ULT_ATUAL_BEM_CANDIDATO    AS dt_ult_atual_bem
FROM {{ ref('silver_bens') }} AS b
-- only assets of candidacies present in the dimension (1st round, APTO)
INNER JOIN {{ ref('gold_dim_candidatura') }} AS c
    ON c.sq_candidato = b.SQ_CANDIDATO
