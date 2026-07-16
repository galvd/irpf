# IRPF · Observatório ES

Dashboard interativo com o perfil agregado dos declarantes de IRPF do Espírito
Santo, por município e por profissão. Dados públicos da Receita Federal,
agregados no nível UF × município × profissão.

## Estrutura

```
irpf/
├── index.html                  GERADO — dashboard pronto, na raiz do projeto (GitHub Pages
│                                serve direto daqui). Pode apagar a qualquer momento e rodar
│                                "python main.py build-dashboard" de novo sem problema.
├── src/
│   ├── main.py                  ponto de entrada do projeto
│   ├── config.py                caminhos do projeto
│   ├── logger.py                configuração de logging
│   ├── occupation_names.py      dicionário de simplificação de nomes de profissão
│   ├── municipality_names.py    dicionário de correção de nomes de município (acentos/grafia)
│   ├── dashboard_template.py    fonte de verdade do design (HTML/CSS/JS como string Python)
│   └── dashboard_builder.py     agrega o CSV + aplica os dicionários + monta o index.html
└── data/
    └── raw/
        └── irpf_municipio_profissao.csv   dado de origem: declarantes por UF × município × profissão
```

**Não existe nenhum arquivo `.html` versionado à parte.** O design completo
(HTML/CSS/JS) mora em `src/dashboard_template.py` como uma string Python
(`TEMPLATE_HTML`). Quer mudar layout, cor ou comportamento do dashboard? Edite
esse arquivo. `index.html`, na raiz, é 100% gerado a partir dele + do CSV — pode
apagar a qualquer momento, rodar o build de novo e ele volta.

## Uso

```
pip install requests
cd src
python main.py build-dashboard
```

Isso lê `data/raw/irpf_municipio_profissao.csv`, aplica os dois dicionários
(profissão e município), calcula as agregações ponderadas por município e por
profissão, e grava `index.html` na raiz do projeto — pronto para abrir no
navegador ou publicar via GitHub Pages.

## Dashboard

`index.html` é autocontido (dados embutidos no próprio arquivo) — abre direto no
navegador, sem servidor.

- Lista de municípios em ordem alfabética (`localeCompare('pt-BR')`, correta
  mesmo com acentos), com uma linha fixa no topo para o agregado do estado
  inteiro (todos os 78 municípios somados, com a própria quebra por profissão
  agregada).
- Cartões de métricas por município e para o estado: feminino, idade média,
  rendimento tributável médio, renda anual média, patrimônio médio e número de
  declarantes.
- Gráfico das top 12 profissões, alternável entre ordenar por número de
  declarantes, renda anual média, renda anual tributável ou patrimônio médio.
  Na visão de renda anual, uma barra sobreposta mostra a parcela tributável em
  valor absoluto (mesma escala), com o percentual entre parênteses no rótulo.
- Nomes de profissão e de município exibidos já passam pelos dicionários de
  simplificação/correção — os nomes originais completos continuam disponíveis
  via tooltip (profissão) ou como chave interna (município).

## Ressalvas dos dados

- Grupos Município × Profissão com menos de 10 declarantes são omitidos pela
  própria Receita (sigilo estatístico). A soma por profissão fica ~1,5% abaixo
  do total oficial do estado.
- Médias não devem ser somadas/promediadas diretamente entre linhas; use média
  ponderada pela coluna `Quantidade` (é o que `dashboard_builder.py` e o
  dashboard fazem).
- Linhas com `Profissao` vazia representam declarantes sem profissão principal
  informada no cadastro, não um subtotal do município.
- Os dicionários de profissão (132 entradas) e de município (78 entradas)
  cobrem 100% do que existe no CSV atual. Nomes que não estiverem catalogados
  caem em fallback (nome original, sem simplificação).

## Projeto relacionado

Este projeto tem uma contraparte voltada ao mercado de trabalho: o **Monitor de
Emprego e Renda** (RAIS_information_loss), que mapeia emprego e densidade
empresarial do Espírito Santo em grade hexagonal, a partir de dados de RAIS e
CNPJ.

- Perfil no GitHub: [github.com/galvd](https://github.com/galvd)
- Repositório do projeto: [github.com/galvd/RAIS_information_loss](https://github.com/galvd/RAIS_information_loss)
- Dashboard com os mapas: [galvd.github.io/RAIS_information_loss](https://galvd.github.io/RAIS_information_loss/)

