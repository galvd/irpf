"""
Constroi os dados agregados usados pelo dashboard a partir do CSV coletado
(config.OUT_CSV), aplicando:
  - occupation_names.simplify(): nome curto de profissao p/ exibicao (mantem o
    nome completo para tooltip)
  - municipality_names.fix_name(): grafia oficial do municipio p/ exibicao
    (mantem o nome bruto como chave interna)
  - media ponderada por Quantidade em todos os agregados por municipio

O HTML final e sempre montado a partir de TEMPLATE_HTML (dashboard_template.py —
fonte de verdade do design em codigo Python, CSS/JS inclusos, sem depender de
nenhum arquivo .html no repositorio) e gravado em index.html na RAIZ do projeto
(config.DASHBOARD_HTML), pronto para servir via GitHub Pages. Por ser regenerado
do zero a cada build, o index.html pode ser apagado a qualquer momento sem
quebrar nada.
"""

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dashboard_template import TEMPLATE_HTML

import config
from occupation_names import simplify
from municipality_names import fix_name


def _weighted_avg(items, key):
    num, den = 0.0, 0
    for it in items:
        if it[key] is not None:
            num += it[key] * it["q"]
            den += it["q"]
    return round(num / den, 4) if den else None


def load_aggregated_data(csv_path=None):
    """Le o CSV combinado e retorna o dict {municipio_bruto: {...}} pronto para
    servir de dado embutido no dashboard."""
    csv_path = csv_path or config.OUT_CSV
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8")))

    municipios = defaultdict(list)
    for r in rows:
        prof_original = r["Profissao"] if r["Profissao"] else "Não informada"
        municipios[r["Municipio"]].append({
            "p": prof_original,     # nome de exibicao (substituido por simplify abaixo)
            "pf": prof_original,    # nome completo (tooltip)
            "q": int(r["Quantidade"]),
            "f": float(r["PctFeminino"]) if r["PctFeminino"] not in ("", None) else None,
            "i": round(float(r["MediaIdade"]), 1) if r["MediaIdade"] not in ("", None) else None,
            "rt": round(float(r["MediaRendTotal"]), 2) if r["MediaRendTotal"] not in ("", None) else None,
            "rb": round(float(r["MediaRendTrib"]), 2) if r["MediaRendTrib"] not in ("", None) else None,
            "pt": round(float(r["MediaPatrimonio"]), 2) if r["MediaPatrimonio"] not in ("", None) else None,
        })

    for items in municipios.values():
        for it in items:
            if it["p"] != "Não informada":
                it["pf"] = it["p"]
                it["p"] = simplify(it["p"])

    out = {}
    for mun, items in municipios.items():
        tq = sum(it["q"] for it in items)
        out[mun] = {
            "disp": fix_name(mun),
            "tq": tq,
            "f": _weighted_avg(items, "f"),
            "i": _weighted_avg(items, "i"),
            "rt": _weighted_avg(items, "rt"),
            "rb": _weighted_avg(items, "rb"),
            "pt": _weighted_avg(items, "pt"),
            # [nome_curto, quantidade, pctfem, idade, rendtotal, rendtrib, patrimonio, nome_completo]
            "profs": [
                [it["p"], it["q"], it["f"], it["i"], it["rt"], it["rb"], it["pt"], it["pf"]]
                for it in sorted(items, key=lambda x: -x["q"])
            ],
        }
    return out


def render_html(data):
    """Injeta o JSON no TEMPLATE_HTML (string Python, dashboard_template.py — fonte
    de verdade do design, sem depender de nenhum arquivo .html no repositorio) e
    devolve o HTML completo. Nao toca em nenhum arquivo — apenas monta a string.
    Falha alto se o marcador nao existir, para nunca gerar um HTML sem dados."""
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    new_html, n = re.subn(
        r'(<script type="application/json" id="irpf-data">).*?(</script>)',
        lambda m: m.group(1) + payload + m.group(2),
        TEMPLATE_HTML,
        count=1,
        flags=re.S,
    )
    if n == 0:
        raise RuntimeError(
            'Marcador <script id="irpf-data"> nao encontrado em TEMPLATE_HTML '
            "(dashboard_template.py). Nada foi gerado."
        )
    return new_html


def build(csv_path=None, output_path=None):
    """Pipeline completo: le o CSV, agrega, monta o HTML a partir do template (em
    codigo) e grava em config.DASHBOARD_HTML (raiz do projeto, para servir via
    GitHub Pages). Regenera o arquivo do zero sempre — pode apagar o index.html a
    qualquer momento e rodar de novo sem quebrar nada; o template vive no codigo,
    nao em um arquivo separado que possa faltar.
    Retorna o numero de municipios processados."""
    data = load_aggregated_data(csv_path)
    html = render_html(data)
    output_path = Path(output_path or config.DASHBOARD_HTML)
    output_path.write_text(html, encoding="utf-8")
    return len(data)


if __name__ == "__main__":
    n = build()
    print(f"dashboard atualizado: {n} municipios")
