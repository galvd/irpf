"""
Configuracao publica: caminhos do projeto. Nao contem nada especifico da coleta
na Receita Federal (isso fica em scraper_config.py, fora do repositorio publico).

Este modulo e usado tanto pelo pipeline de coleta (collector.py) quanto pelo
pipeline do dashboard (dashboard_builder.py, main.py) — precisa continuar
funcionando mesmo quando os arquivos de coleta nao estiverem presentes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_CHECKPOINTS = ROOT / "data" / "checkpoints"
DATA_LOGS = ROOT / "data" / "logs"
for _d in (DATA_RAW, DATA_CHECKPOINTS, DATA_LOGS):
    _d.mkdir(parents=True, exist_ok=True)

OUT_CSV = DATA_RAW / "irpf_municipio_profissao.csv"
CHECKPOINT = DATA_CHECKPOINTS / "checkpoint_combinado.json"
LOG_FILE = DATA_LOGS / "coleta_combinado.log"
DEBUG_JSON = DATA_RAW / "debug_combinado.json"
DASHBOARD_HTML = ROOT / "index.html"
