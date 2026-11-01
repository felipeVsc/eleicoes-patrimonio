"""Gera os gráficos do README (docs/img/) a partir da camada gold.

Cada gráfico sai em duas versões, clara e escura, que o README alterna com <picture>.
O dbt precisa ter rodado antes (o banco é aberto somente para leitura).

Uso: uv run scripts/graficos.py
"""

from pathlib import Path

import duckdb
import matplotlib.pyplot as plt

RAIZ = Path(__file__).parents[1]
SAIDA = RAIZ / "docs/img"

TEMAS = {
    "claro": {"fundo": "#fcfcfb", "texto": "#0b0b0b", "texto2": "#52514e", "barra": "#2a78d6"},
    "escuro": {"fundo": "#1a1a19", "texto": "#f0efec", "texto2": "#c3c2b7", "barra": "#3987e5"},
}

# patrimônio total por candidatura (apenas quem declarou bens)
PATRIMONIO_2022 = """
    SELECT c.*, SUM(f.vr_bem) AS vr_patrimonio
    FROM gold.gold_fact_bem_candidato f
    JOIN gold.gold_dim_candidatura c USING (sq_candidato)
    WHERE c.ano_eleicao = 2022
    GROUP BY ALL
"""


def reais(v):
    if v >= 1e6:
        return f"R$ {v / 1e6:.1f} mi".replace(".", ",")
    return f"R$ {v / 1e3:.0f} mil"


GRAFICOS = {
    "mediana_cor_raca": {
        "titulo": "Mediana do patrimônio declarado por cor/raça (2022)",
        "subtitulo": "Candidaturas aptas no 1º turno que declararam bens",
        "sql": f"""
            SELECT ds_cor_raca AS rotulo, MEDIAN(vr_patrimonio) AS valor
            FROM ({PATRIMONIO_2022})
            WHERE ds_cor_raca <> 'NÃO INFORMADO'
            GROUP BY 1 ORDER BY 2
        """,
        "formato": reais,
    },
    "mediana_cargo": {
        "titulo": "Mediana do patrimônio declarado por cargo (2022)",
        "subtitulo": "Candidaturas aptas no 1º turno que declararam bens",
        "sql": f"""
            SELECT ds_cargo AS rotulo, MEDIAN(vr_patrimonio) AS valor
            FROM ({PATRIMONIO_2022})
            GROUP BY 1 ORDER BY 2
        """,
        "formato": reais,
    },
    "composicao_categoria": {
        "titulo": "Onde está o patrimônio dos candidatos",
        "subtitulo": "Participação de cada categoria no valor total declarado, 2018 + 2022",
        "sql": """
            SELECT t.ds_categoria AS rotulo, SUM(f.vr_bem) / SUM(SUM(f.vr_bem)) OVER () AS valor
            FROM gold.gold_fact_bem_candidato f
            JOIN gold.gold_dim_tipo_bem t USING (cd_tipo_bem)
            GROUP BY 1 ORDER BY 2
        """,
        "formato": lambda v: f"{v:.1%}".replace(".", ","),
    },
}


def desenhar(df, grafico, tema, arquivo):
    cores = TEMAS[tema]
    fig, ax = plt.subplots(figsize=(9, 0.42 * len(df) + 1.4), dpi=150)
    fig.patch.set_facecolor(cores["fundo"])
    ax.set_facecolor(cores["fundo"])

    barras = ax.barh(df["rotulo"], df["valor"], height=0.6, color=cores["barra"])
    for barra, valor in zip(barras, df["valor"]):
        ax.text(barra.get_width(), barra.get_y() + barra.get_height() / 2, "  " + grafico["formato"](valor),
                va="center", ha="left", fontsize=9, color=cores["texto2"])

    ax.set_xlim(0, df["valor"].max() * 1.25)
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0, labelsize=9, labelcolor=cores["texto"])
    for lado in ax.spines.values():
        lado.set_visible(False)

    fig.text(0.01, 0.98, grafico["titulo"], ha="left", va="top", fontsize=12, fontweight="bold", color=cores["texto"])
    fig.text(0.01, 0.98 - 0.32 / fig.get_figheight(), grafico["subtitulo"], ha="left", va="top",
             fontsize=9, color=cores["texto2"])
    fig.tight_layout(rect=(0, 0, 1, 1 - 0.6 / fig.get_figheight()))
    fig.savefig(arquivo, facecolor=cores["fundo"])
    plt.close(fig)


con = duckdb.connect(str(RAIZ / "eleicoes.duckdb"), read_only=True)
SAIDA.mkdir(parents=True, exist_ok=True)
for nome, grafico in GRAFICOS.items():
    df = con.sql(grafico["sql"]).df()
    for tema in TEMAS:
        desenhar(df, grafico, tema, SAIDA / f"{nome}_{tema}.png")
        print(SAIDA / f"{nome}_{tema}.png")
