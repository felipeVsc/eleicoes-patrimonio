{#
    Surrogate key for a person: hash of the CPF. When the CPF is not disclosed
    (TSE publishes '-4'), falls back to the candidacy id, so those people can't
    be tracked across elections.
    hash() returns UBIGINT; shifting one bit makes it fit a signed BIGINT, which
    BI tools such as Superset (pyarrow) can read.
#}
{% macro sk_pessoa(cpf_column='NR_CPF_CANDIDATO', sq_column='SQ_CANDIDATO') %}
    CAST(hash(
        CASE
            WHEN regexp_full_match({{ cpf_column }}, '[0-9]{11}') THEN {{ cpf_column }}
            ELSE 'SQ:' || CAST({{ sq_column }} AS VARCHAR)
        END
    ) >> 1 AS BIGINT)
{% endmacro %}
