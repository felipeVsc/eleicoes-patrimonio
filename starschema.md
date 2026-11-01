# Modelo dimensional: patrimônio declarado pelos candidatos

Fontes: `silver_candidatos` (consulta_cand, apenas 1º turno e situação APTO) e `silver_bens`
(bem_candidato). Eleições de 2018 e 2022. O SQL está em [eleicoes/models/gold/](eleicoes/models/gold/).

Pipeline: CSVs → schema `bronze` (staging, carregado como está pelo main.ipynb) → silver (dbt) → gold (dbt).

```
                    dim_eleicao
                         |
dim_tipo_bem ---- fact_bem_candidato ---- dim_candidatura
                         |
                     dim_pessoa
```

## Fato

**gold_fact_bem_candidato**: grão = um bem declarado por uma candidatura

| coluna | observação |
|---|---|
| cd_eleicao | FK → dim_eleicao |
| sq_candidato | FK → dim_candidatura |
| sk_pessoa | FK → dim_pessoa |
| cd_tipo_bem | FK → dim_tipo_bem |
| ano_eleicao | desnormalizado para facilitar filtros |
| nr_ordem_bem | dimensão degenerada |
| ds_bem | dimensão degenerada (descrição livre) |
| vr_bem | medida, DECIMAL(18,2), R$ nominais |
| dt_ult_atual_bem | última atualização da declaração |

Só entram bens de candidaturas presentes em `dim_candidatura` (1º turno, APTO).

## Dimensões

**gold_dim_eleicao**: uma linha por eleição (`cd_eleicao`)
ano_eleicao, cd_tipo_eleicao, nm_tipo_eleicao, ds_eleicao, dt_eleicao

**gold_dim_tipo_bem**: uma linha por tipo de bem do TSE (`cd_tipo_bem`, ~50 códigos, estáveis entre 2018 e 2022)
ds_tipo_bem e ds_categoria (macrocategoria derivada da faixa do código):

| códigos | ds_categoria |
|---|---|
| 1–19 | Imóveis |
| 21–23 | Veículos, aeronaves e embarcações |
| 24–29 | Outros bens móveis |
| 31–39 | Participações societárias |
| 41–49, 71–79, 97 | Aplicações financeiras e fundos |
| 51–59 | Créditos e poupança vinculada |
| 61, 62, 65–69 | Depósitos bancários |
| 63, 64 | Dinheiro em espécie |
| demais (91–99 exceto 97) | Outros bens e direitos |

**gold_dim_candidatura**: uma linha por candidatura (`sq_candidato`), com os atributos que podem mudar entre eleições
cd_eleicao, ano_eleicao, sk_pessoa, nr_candidato, nm_candidato, nm_urna_candidato,
dt_nascimento, sg_uf_nascimento, ds_genero, ds_cor_raca,
cd_cargo, ds_cargo, sg_uf, sg_ue, nm_ue,
nr_partido, sg_partido, nm_partido, sg_federacao,
cd_situacao_candidatura, ds_situacao_candidatura,
ds_grau_instrucao, ds_ocupacao, ds_estado_civil

**gold_dim_pessoa**: uma linha por pessoa (`sk_pessoa`), apenas identidade
nr_cpf, qt_candidaturas, ano_primeira_candidatura, ano_ultima_candidatura

Nome, cor/raça, gênero etc. são declarados a cada candidatura e mudam (cerca de 1,2 mil pessoas
mudaram cor/raça ou nome entre 2018 e 2022), por isso ficam em `dim_candidatura`. Para comparar as
candidaturas de uma pessoa, faça um *self-join* de `dim_candidatura` em `sk_pessoa`.

`sk_pessoa = hash(cpf)` (macro `sk_pessoa`). Quando o CPF não é divulgado (o TSE publica `-4`),
usa `hash('SQ:' || sq_candidato)`, e essa pessoa não pode ser acompanhada entre eleições.

## Análise → tabela

| análise | tabelas |
|---|---|
| maiores patrimônios; por partido, cargo, profissão, escolaridade, gênero, cor/raça | fato + dim_candidatura |
| evolução patrimonial entre eleições | fato + dim_candidatura (self-join em sk_pessoa) |
| itens mais caros, categorias com maior valor | fato + dim_tipo_bem + dim_candidatura |

Planejado: tabelas agregadas para o Superset (`agg_patrimonio_candidatura`, incluindo
candidaturas sem bens, e `agg_evolucao_patrimonial`).

## Cuidados

- Valores nominais: comparar 2018 com 2022 sem correção pelo IPCA superestima o crescimento.
- O patrimônio é muito assimétrico: prefira medianas e escala logarítmica. Muitos candidatos não
  declaram nada (eles não aparecem na fato, só em `dim_candidatura`).
- Em 2018 a descrição livre (`ds_bem`) é quase sempre `#NULO`; use `ds_tipo_bem`.
