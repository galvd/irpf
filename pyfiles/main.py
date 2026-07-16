#!/usr/bin/env python3
"""
Orquestrador do projeto IRPF - Observatorio ES.

Comandos:
  python main.py collect              coleta dados do painel (todas as UFs, continua checkpoint)
  python main.py collect --ufs ES      restringe a UF(s) especificas
  python main.py collect --fresh       apaga CSV+checkpoint e comeca do zero
  python main.py collect --debug       roda so ES, salva JSON cru p/ conferencia (nao grava CSV)

  python main.py build-dashboard        monta index.html (raiz do projeto) a partir do CSV atual
                                         (aplica dicionarios de profissao/municipio + agregacoes)

  python main.py all                    coleta e, ao final, reconstroi o dashboard
  python main.py all --ufs ES --fresh   idem, com as mesmas opcoes de coleta

Sem argumentos, mostra esta ajuda.
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
import dashboard_builder


def _load_collector():
    """Import tardio de collector.py: os scripts de coleta da Receita Federal
    nao fazem parte do repositorio publico (ver .gitignore). Isso deixa
    'build-dashboard' funcionando em qualquer checkout, mesmo sem eles, e falha
    com uma mensagem clara (em vez de traceback) quando 'collect'/'all' e
    chamado num checkout que nao tem esses arquivos."""
    try:
        import collector
        return collector
    except ImportError:
        print(
            "Modulo de coleta (collector.py e afins) nao encontrado neste checkout.\n"
            "Os scripts que coletam dados da Receita Federal nao fazem parte do "
            "repositorio publico — ficam apenas na copia local de quem roda a coleta.\n"
            "'build-dashboard' continua funcionando normalmente a partir do CSV existente."
        )
        sys.exit(1)


def cmd_collect(args):
    if args.fresh:
        for f in (config.OUT_CSV, config.CHECKPOINT):
            if f.exists():
                f.unlink()
                print(f"removido: {f}")

    collector = _load_collector()

    if args.debug:
        collector.run_debug()
        return

    ufs = collector.resolve_ufs(args.ufs)
    collector.run_collection(ufs)


def cmd_build_dashboard(args):
    n = dashboard_builder.build()
    print(f"dashboard atualizado: {n} municipios (fonte: {config.OUT_CSV})")


def cmd_all(args):
    cmd_collect(args)
    if args.debug:
        return  # --debug nao gera CSV; nao ha o que reconstruir no dashboard
    cmd_build_dashboard(args)


def build_parser():
    parser = argparse.ArgumentParser(
        description="Orquestrador do pipeline IRPF - Observatorio ES (coleta + dashboard)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    def add_collect_args(p):
        p.add_argument("--ufs", help="UFs separadas por virgula (ex: ES ou ES,RJ). Default: todas.")
        p.add_argument("--fresh", action="store_true", help="apaga CSV e checkpoint antes de coletar")
        p.add_argument("--debug", action="store_true", help="roda so ES, salva JSON cru, nao grava CSV")

    p_collect = sub.add_parser("collect", help="Coleta dados do painel (UF x Municipio x Ocupacao Principal)")
    add_collect_args(p_collect)
    p_collect.set_defaults(func=cmd_collect)

    p_build = sub.add_parser(
        "build-dashboard",
        help="Reconstroi os dados embutidos em dashboard/index.html a partir do CSV atual",
    )
    p_build.set_defaults(func=cmd_build_dashboard)

    p_all = sub.add_parser("all", help="Coleta e, em seguida, reconstroi o dashboard")
    add_collect_args(p_all)
    p_all.set_defaults(func=cmd_all)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
