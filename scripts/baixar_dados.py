"""Baixa os dados abertos do TSE usados no projeto para eleicoes/data/raw/.

De cada .zip do TSE extrai apenas o arquivo nacional (<conjunto>_<ano>_BRASIL.csv),
que é o único lido pelo main.ipynb.

Uso: uv run scripts/baixar_dados.py [destino]
"""

import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

BASE_URL = "https://cdn.tse.jus.br/estatistica/sead/odsele"
CONJUNTOS = ["consulta_cand", "bem_candidato"]
ANOS = [2018, 2022]

destino = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parents[1] / "eleicoes/data/raw"

for conjunto in CONJUNTOS:
    for ano in ANOS:
        nome = f"{conjunto}_{ano}"
        csv = f"{nome}_BRASIL.csv"
        saida = destino / nome / csv
        if saida.exists():
            print(f"{csv}: já existe, pulando")
            continue

        url = f"{BASE_URL}/{conjunto}/{nome}.zip"
        print(f"{csv}: baixando {url}")
        with tempfile.TemporaryFile() as tmp:
            with urllib.request.urlopen(url) as resp:
                shutil.copyfileobj(resp, tmp)
            with zipfile.ZipFile(tmp) as zf:
                saida.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(csv) as src, open(saida, "wb") as dst:
                    shutil.copyfileobj(src, dst)
