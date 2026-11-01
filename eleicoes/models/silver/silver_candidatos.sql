select * from {{ source('eleicoes', 'candidatos') }} 
where NR_TURNO = 1 and DS_SITUACAO_CANDIDATURA = 'APTO'
