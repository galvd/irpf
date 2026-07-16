"""
Dicionario de correcao dos nomes de municipio do painel IRPF.

A Receita Federal publica os nomes de municipio em CAIXA ALTA e sem acentuacao
(ex.: "AFONSO CLAUDIO", "SAO JOSE DO CALCADO"). Este modulo mapeia cada nome bruto
para a grafia oficial correta (acentos, cedilhas, capitalizacao de nome proprio),
usada apenas para EXIBICAO — o nome bruto permanece como chave interna de dados
(comparacoes, ordenacao, chaves de dicionario) para nao quebrar nada que dependa dele.

Cobre os 78 municipios do Espirito Santo, extraidos de
data/raw/irpf_municipio_profissao.csv.
"""

MUNICIPALITY_NAME_FIXES = {
    "AFONSO CLAUDIO": "Afonso Cláudio",
    "AGUA DOCE DO NORTE": "Água Doce do Norte",
    "AGUIA BRANCA": "Águia Branca",
    "ALEGRE": "Alegre",
    "ALFREDO CHAVES": "Alfredo Chaves",
    "ALTO RIO NOVO": "Alto Rio Novo",
    "ANCHIETA": "Anchieta",
    "APIACA": "Apiacá",
    "ARACRUZ": "Aracruz",
    "ATILIO VIVACQUA": "Atílio Vivácqua",
    "BAIXO GUANDU": "Baixo Guandu",
    "BARRA DE SAO FRANCISCO": "Barra de São Francisco",
    "BOA ESPERANCA": "Boa Esperança",
    "BOM JESUS DO NORTE": "Bom Jesus do Norte",
    "BREJETUBA": "Brejetuba",
    "CACHOEIRO DE ITAPEMIRIM": "Cachoeiro de Itapemirim",
    "CARIACICA": "Cariacica",
    "CASTELO": "Castelo",
    "COLATINA": "Colatina",
    "CONCEICAO DA BARRA": "Conceição da Barra",
    "CONCEICAO DO CASTELO": "Conceição do Castelo",
    "DIVINO DE SAO LOURENCO": "Divino de São Lourenço",
    "DOMINGOS MARTINS": "Domingos Martins",
    "DORES DO RIO PRETO": "Dores do Rio Preto",
    "ECOPORANGA": "Ecoporanga",
    "FUNDAO": "Fundão",
    "GOVERNADOR LINDENBERG": "Governador Lindenberg",
    "GUACUI": "Guaçuí",
    "GUARAPARI": "Guarapari",
    "IBATIBA": "Ibatiba",
    "IBIRACU": "Ibiraçu",
    "IBITIRAMA": "Ibitirama",
    "ICONHA": "Iconha",
    "IRUPI": "Irupi",
    "ITAGUACU": "Itaguaçu",
    "ITAPEMIRIM": "Itapemirim",
    "ITARANA": "Itarana",
    "IUNA": "Iúna",
    "JAGUARE": "Jaguaré",
    "JERONIMO MONTEIRO": "Jerônimo Monteiro",
    "JOAO NEIVA": "João Neiva",
    "LARANJA DA TERRA": "Laranja da Terra",
    "LINHARES": "Linhares",
    "MANTENOPOLIS": "Mantenópolis",
    "MARATAIZES": "Marataízes",
    "MARECHAL FLORIANO": "Marechal Floriano",
    "MARILANDIA": "Marilândia",
    "MIMOSO DO SUL": "Mimoso do Sul",
    "MONTANHA": "Montanha",
    "MUCURICI": "Mucurici",
    "MUNIZ FREIRE": "Muniz Freire",
    "MUQUI": "Muqui",
    "NOVA VENECIA": "Nova Venécia",
    "PANCAS": "Pancas",
    "PEDRO CANARIO": "Pedro Canário",
    "PINHEIROS": "Pinheiros",
    "PIUMA": "Piúma",
    "PONTO BELO": "Ponto Belo",
    "PRESIDENTE KENNEDY": "Presidente Kennedy",
    "RIO BANANAL": "Rio Bananal",
    "RIO NOVO DO SUL": "Rio Novo do Sul",
    "SANTA LEOPOLDINA": "Santa Leopoldina",
    "SANTA MARIA DE JETIBA": "Santa Maria de Jetibá",
    "SANTA TERESA": "Santa Teresa",
    "SAO DOMINGOS DO NORTE": "São Domingos do Norte",
    "SAO GABRIEL DA PALHA": "São Gabriel da Palha",
    "SAO JOSE DO CALCADO": "São José do Calçado",
    "SAO MATEUS": "São Mateus",
    "SAO ROQUE DO CANAA": "São Roque do Canaã",
    "SERRA": "Serra",
    "SOORETAMA": "Sooretama",
    "VARGEM ALTA": "Vargem Alta",
    "VENDA NOVA DO IMIGRANTE": "Venda Nova do Imigrante",
    "VIANA": "Viana",
    "VILA PAVAO": "Vila Pavão",
    "VILA VALERIO": "Vila Valério",
    "VILA VELHA": "Vila Velha",
    "VITORIA": "Vitória",
}


def fix_name(nome_bruto):
    """Retorna a grafia oficial correta; se o municipio nao estiver catalogado
    (ex.: veio de outra UF ainda nao mapeada), devolve o nome bruto sem alteracao."""
    if nome_bruto is None:
        return nome_bruto
    return MUNICIPALITY_NAME_FIXES.get(nome_bruto, nome_bruto)
