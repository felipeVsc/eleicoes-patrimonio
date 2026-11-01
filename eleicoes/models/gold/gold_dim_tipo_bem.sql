SELECT
    CD_TIPO_BEM_CANDIDATO                   AS cd_tipo_bem,
    ANY_VALUE(DS_TIPO_BEM_CANDIDATO)        AS ds_tipo_bem,
    CASE
        WHEN CD_TIPO_BEM_CANDIDATO BETWEEN 1 AND 19  THEN 'Imóveis'
        WHEN CD_TIPO_BEM_CANDIDATO BETWEEN 21 AND 23 THEN 'Veículos, aeronaves e embarcações'
        WHEN CD_TIPO_BEM_CANDIDATO BETWEEN 24 AND 29 THEN 'Outros bens móveis'
        WHEN CD_TIPO_BEM_CANDIDATO BETWEEN 31 AND 39 THEN 'Participações societárias'
        WHEN CD_TIPO_BEM_CANDIDATO BETWEEN 41 AND 49
          OR CD_TIPO_BEM_CANDIDATO BETWEEN 71 AND 79
          OR CD_TIPO_BEM_CANDIDATO = 97              THEN 'Aplicações financeiras e fundos'
        WHEN CD_TIPO_BEM_CANDIDATO BETWEEN 51 AND 59 THEN 'Créditos e poupança vinculada'
        WHEN CD_TIPO_BEM_CANDIDATO IN (63, 64)       THEN 'Dinheiro em espécie'
        WHEN CD_TIPO_BEM_CANDIDATO BETWEEN 61 AND 69 THEN 'Depósitos bancários'
        ELSE 'Outros bens e direitos'
    END                                     AS ds_categoria
FROM {{ ref('silver_bens') }}
GROUP BY CD_TIPO_BEM_CANDIDATO
