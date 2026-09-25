"""Base didatica de minerais usada pelo DrStone.

Os valores sao aproximados e servem apenas para demonstrar o funcionamento da
linguagem. Este catalogo nao deve ser usado para identificacao mineralogica
profissional.
"""

from dataclasses import dataclass
from unicodedata import combining, normalize


@dataclass(frozen=True)
class Mineral:
    """Propriedades de referencia de um mineral conhecido."""

    nome: str
    dureza_min: float
    dureza_max: float
    densidade_min: float
    densidade_max: float
    cor: str
    brilho: str


_LEGACY_MINERALS: tuple[Mineral, ...] = (
    Mineral(
        nome="Quartzo",
        dureza_min=7.0,
        dureza_max=7.0,
        densidade_min=2.60,
        densidade_max=2.70,
        cor="incolor, branca ou variada",
        brilho="vitreo",
    ),
    Mineral(
        nome="Talco",
        dureza_min=1.0,
        dureza_max=1.0,
        densidade_min=2.58,
        densidade_max=2.83,
        cor="branca, cinza ou verde",
        brilho="perolado",
    ),
    Mineral(
        nome="Gipsita",
        dureza_min=2.0,
        dureza_max=2.0,
        densidade_min=2.30,
        densidade_max=2.40,
        cor="incolor ou branca",
        brilho="vitreo ou perolado",
    ),
    Mineral(
        nome="Feldspato",
        dureza_min=6.0,
        dureza_max=6.5,
        densidade_min=2.55,
        densidade_max=2.76,
        cor="branca, rosa ou cinza",
        brilho="vitreo ou perolado",
    ),
    Mineral(
        nome="Topázio",
        dureza_min=8.0,
        dureza_max=8.0,
        densidade_min=3.49,
        densidade_max=3.57,
        cor="incolor, amarela, azul ou rosa",
        brilho="vitreo",
    ),
    Mineral(
        nome="Coríndon",
        dureza_min=9.0,
        dureza_max=9.0,
        densidade_min=3.95,
        densidade_max=4.10,
        cor="cinza, vermelha ou azul",
        brilho="vitreo ou adamantino",
    ),
)


# Campos importados de Dr_Stone_Base_Gemologica_100_Pedras.xlsx:
# nome, Mohs min/max, densidade min/max, cores tipicas e brilho.
_GEM_DATA: tuple[tuple[str, float, float, float, float, str, str], ...] = (
    ("Diamante", 10.0, 10.0, 3.51, 3.53, "incolor; amarelo; marrom; azul; rosa; verde", "adamantino"),
    ("Rubi", 9.0, 9.0, 3.97, 4.05, "vermelho; vermelho-púrpura", "vítreo"),
    ("Safira azul", 9.0, 9.0, 3.95, 4.03, "azul", "vítreo"),
    ("Safira rosa", 9.0, 9.0, 3.95, 4.03, "rosa", "vítreo"),
    ("Safira amarela", 9.0, 9.0, 3.95, 4.03, "amarelo", "vítreo"),
    ("Safira verde", 9.0, 9.0, 3.95, 4.03, "verde", "vítreo"),
    ("Safira branca", 9.0, 9.0, 3.95, 4.03, "incolor", "vítreo"),
    ("Espinélio vermelho", 8.0, 8.0, 3.54, 3.7, "vermelho", "vítreo"),
    ("Espinélio azul", 8.0, 8.0, 3.54, 3.7, "azul", "vítreo"),
    ("Espinélio rosa", 8.0, 8.0, 3.54, 3.7, "rosa", "vítreo"),
    ("Esmeralda", 7.5, 8.0, 2.67, 2.78, "verde; verde-azulado", "vítreo"),
    ("Água-marinha", 7.5, 8.0, 2.68, 2.74, "azul-claro; azul-esverdeado", "vítreo"),
    ("Morganita", 7.5, 8.0, 2.71, 2.9, "rosa; pêssego", "vítreo"),
    ("Heliodoro", 7.5, 8.0, 2.68, 2.8, "amarelo; dourado", "vítreo"),
    ("Goshenita", 7.5, 8.0, 2.68, 2.8, "incolor", "vítreo"),
    ("Ametista", 7.0, 7.0, 2.64, 2.66, "violeta; púrpura", "vítreo"),
    ("Citrino", 7.0, 7.0, 2.64, 2.66, "amarelo; laranja; marrom-amarelado", "vítreo"),
    ("Quartzo rosa", 7.0, 7.0, 2.64, 2.66, "rosa", "vítreo"),
    ("Cristal de rocha", 7.0, 7.0, 2.64, 2.66, "incolor", "vítreo"),
    ("Quartzo fumê", 7.0, 7.0, 2.64, 2.66, "marrom; cinza; quase preto", "vítreo"),
    ("Ametrino", 7.0, 7.0, 2.64, 2.66, "violeta e amarelo", "vítreo"),
    ("Prasiolita", 7.0, 7.0, 2.64, 2.66, "verde-claro", "vítreo"),
    ("Calcedônia", 6.5, 7.0, 2.58, 2.64, "branco; cinza; azul; variado", "ceroso a vítreo"),
    ("Ágata", 6.5, 7.0, 2.58, 2.64, "bandada; multicolorida", "ceroso"),
    ("Ônix", 6.5, 7.0, 2.58, 2.64, "preto; branco em bandas", "ceroso"),
    ("Cornalina", 6.5, 7.0, 2.58, 2.64, "laranja; vermelho-acastanhado", "ceroso"),
    ("Crisoprásio", 6.5, 7.0, 2.58, 2.64, "verde-maçã", "ceroso"),
    ("Jaspe", 6.5, 7.0, 2.55, 2.91, "vermelho; amarelo; marrom; verde", "ceroso a vítreo"),
    ("Topázio incolor", 8.0, 8.0, 3.49, 3.57, "incolor", "vítreo"),
    ("Topázio azul", 8.0, 8.0, 3.49, 3.57, "azul", "vítreo"),
    ("Topázio imperial", 8.0, 8.0, 3.49, 3.57, "laranja; rosa-alaranjado; dourado", "vítreo"),
    ("Turmalina rubelita", 7.0, 7.5, 3.0, 3.15, "rosa; vermelho", "vítreo"),
    ("Turmalina indicolita", 7.0, 7.5, 3.0, 3.2, "azul; azul-esverdeado", "vítreo"),
    ("Turmalina verdelita", 7.0, 7.5, 3.0, 3.2, "verde", "vítreo"),
    ("Turmalina Paraíba", 7.0, 7.5, 3.0, 3.12, "azul-neon; verde-azulado", "vítreo"),
    ("Schorl", 7.0, 7.5, 3.1, 3.3, "preto", "vítreo"),
    ("Peridoto", 6.5, 7.0, 3.27, 3.37, "verde-amarelado", "vítreo"),
    ("Granada almandina", 7.0, 7.5, 3.95, 4.32, "vermelho escuro; vermelho-marrom", "vítreo"),
    ("Granada piropo", 7.0, 7.5, 3.58, 3.84, "vermelho; vermelho-púrpura", "vítreo"),
    ("Rodolita", 7.0, 7.5, 3.74, 3.94, "rosa-avermelhado; púrpura", "vítreo"),
    ("Granada grossulária", 6.5, 7.5, 3.49, 3.73, "incolor; amarelo; verde; laranja", "vítreo"),
    ("Tsavorita", 6.5, 7.5, 3.55, 3.73, "verde vivo", "vítreo"),
    ("Hessonita", 6.5, 7.5, 3.57, 3.73, "laranja; canela; marrom", "vítreo"),
    ("Demantoide", 6.5, 7.0, 3.8, 3.9, "verde", "adamantino"),
    ("Spessartina", 7.0, 7.5, 4.05, 4.2, "laranja; laranja-avermelhado", "vítreo"),
    ("Zircão incolor", 6.0, 7.5, 4.6, 4.75, "incolor", "adamantino"),
    ("Zircão azul", 6.0, 7.5, 4.6, 4.75, "azul", "adamantino"),
    ("Zircão marrom", 6.0, 7.5, 4.0, 4.75, "marrom; vermelho-marrom", "adamantino"),
    ("Tanzanita", 6.0, 7.0, 3.3, 3.38, "azul; violeta", "vítreo"),
    ("Zoisita verde", 6.0, 7.0, 3.25, 3.38, "verde", "vítreo"),
    ("Iolita", 7.0, 7.5, 2.58, 2.66, "azul-violeta; cinza-azulado", "vítreo"),
    ("Kunzita", 6.5, 7.0, 3.15, 3.21, "rosa; lilás", "vítreo"),
    ("Hiddenita", 6.5, 7.0, 3.15, 3.21, "verde", "vítreo"),
    ("Jadeíta", 6.5, 7.0, 3.25, 3.4, "verde; branco; lilás; amarelo", "vítreo a gorduroso"),
    ("Nefrita", 6.0, 6.5, 2.9, 3.1, "verde; branco; cinza", "gorduroso"),
    ("Pedra-da-lua", 6.0, 6.5, 2.55, 2.63, "incolor; branco; pêssego; cinza", "vítreo"),
    ("Labradorita", 6.0, 6.5, 2.68, 2.72, "cinza; azul/verde iridescente", "vítreo"),
    ("Sunstone ortoclásio", 6.0, 7.2, 2.56, 2.6, "amarelo; laranja; vermelho", "vítreo"),
    ("Sunstone oligoclásio", 6.0, 7.2, 2.63, 2.67, "amarelo; laranja; vermelho", "vítreo"),
    ("Sunstone labradorita", 6.0, 7.2, 2.68, 2.72, "verde; vermelho; laranja", "vítreo"),
    ("Opala branca", 5.0, 6.5, 1.25, 2.23, "branco; multicolorido", "vítreo a resinoso"),
    ("Opala negra", 5.0, 6.5, 1.25, 2.23, "base escura; jogo de cores", "vítreo a resinoso"),
    ("Opala de fogo", 5.0, 6.5, 1.25, 2.23, "amarelo; laranja; vermelho", "vítreo"),
    ("Turquesa", 5.0, 6.0, 2.6, 2.9, "azul; azul-esverdeado; verde", "ceroso"),
    ("Lápis-lazúli", 5.0, 5.5, 2.7, 2.9, "azul ultramarino", "vítreo a gorduroso"),
    ("Sodalita", 5.5, 6.0, 2.14, 2.4, "azul; violeta; branco", "vítreo a gorduroso"),
    ("Obsidiana", 5.0, 5.5, 2.3, 2.6, "preto; marrom; verde; arco-íris", "vítreo"),
    ("Malaquita", 3.5, 4.0, 3.6, 4.05, "verde bandado", "vítreo a sedoso"),
    ("Azurita", 3.5, 4.0, 3.7, 3.9, "azul profundo", "vítreo"),
    ("Calcita", 3.0, 3.0, 2.69, 2.71, "incolor; branco; amarelo; variado", "vítreo"),
    ("Fluorita", 4.0, 4.0, 3.17, 3.18, "roxo; verde; azul; amarelo; incolor", "vítreo"),
    ("Apatita", 5.0, 5.0, 3.16, 3.22, "verde; azul; amarelo; roxo", "vítreo"),
    ("Apatita Paraíba-like", 5.0, 5.0, 3.16, 3.22, "azul-neon; verde-azulado", "vítreo"),
    ("Crisoberilo", 8.5, 8.5, 3.7, 3.78, "amarelo; verde; marrom", "vítreo"),
    ("Alexandrita", 8.5, 8.5, 3.7, 3.78, "verde à luz do dia; vermelho sob incandescente", "vítreo"),
    ("Olho-de-gato crisoberilo", 8.5, 8.5, 3.7, 3.78, "amarelo; verde; marrom", "vítreo"),
    ("Diopsídio", 5.5, 6.5, 3.22, 3.38, "verde; incolor; marrom", "vítreo"),
    ("Diopsídio cromífero", 5.5, 6.5, 3.22, 3.38, "verde intenso", "vítreo"),
    ("Enstatita", 5.0, 6.0, 3.2, 3.3, "verde; marrom; amarelo", "vítreo"),
    ("Prehnita", 6.0, 6.5, 2.8, 2.95, "verde-claro; amarelo; incolor", "vítreo a perolado"),
    ("Rodocrosita", 3.5, 4.0, 3.45, 3.7, "rosa; vermelho-rosado; bandado", "vítreo a perolado"),
    ("Rodonita", 5.5, 6.5, 3.4, 3.76, "rosa; vermelho-rosado com preto", "vítreo"),
    ("Amazonita", 6.0, 6.5, 2.54, 2.57, "verde; azul-esverdeado", "vítreo"),
    ("Aventurina verde", 6.5, 7.0, 2.64, 2.69, "verde com brilho aventurescente", "vítreo"),
    ("Hematita", 5.0, 6.5, 4.9, 5.3, "cinza metálico; preto; vermelho-marrom", "metálico"),
    ("Magnetita", 5.5, 6.5, 5.1, 5.2, "preto", "metálico"),
    ("Pirita", 6.0, 6.5, 4.9, 5.2, "dourado metálico", "metálico"),
    ("Âmbar", 2.0, 2.5, 1.05, 1.1, "amarelo; laranja; marrom; verde", "resinoso"),
    ("Pérola", 2.5, 4.5, 2.6, 2.85, "branco; creme; rosa; preto; dourado", "perolado"),
    ("Coral precioso", 3.0, 4.0, 2.6, 2.7, "vermelho; rosa; branco", "vítreo a ceroso"),
    ("Serpentina", 2.5, 5.5, 2.44, 2.62, "verde; amarelo; branco", "gorduroso"),
    ("Chrysocolla", 2.0, 4.0, 2.0, 2.4, "azul; verde; azul-esverdeado", "vítreo a terroso"),
    ("Larimar", 4.5, 5.0, 2.74, 2.9, "azul-claro; branco", "sedoso a vítreo"),
    ("Charoíta", 5.0, 6.0, 2.54, 2.78, "violeta; lilás com padrões fibrosos", "vítreo a sedoso"),
    ("Sugilita", 5.5, 6.5, 2.74, 2.8, "violeta; púrpura", "vítreo"),
    ("Kyanita azul", 4.5, 7.0, 3.53, 3.67, "azul; azul-esverdeado", "vítreo"),
    ("Andaluzita", 6.5, 7.5, 3.13, 3.18, "marrom; verde; amarelo; rosa", "vítreo"),
    ("Sillimanita", 6.5, 7.5, 3.23, 3.27, "incolor; amarelo; verde; marrom", "vítreo"),
    ("Escapolita", 5.5, 6.0, 2.55, 2.8, "amarelo; rosa; violeta; incolor", "vítreo"),
    ("Benitoíta", 6.0, 6.5, 3.64, 3.68, "azul; violeta; incolor", "vítreo a adamantino"),
)


MINERALS: tuple[Mineral, ...] = _LEGACY_MINERALS + tuple(
    Mineral(*values) for values in _GEM_DATA
)


def _normalize_name(name: str) -> str:
    decomposed = normalize("NFKD", name.strip().casefold())
    return "".join(character for character in decomposed if not combining(character))


_MINERALS_BY_NAME = {_normalize_name(mineral.nome): mineral for mineral in MINERALS}


def get_mineral(name: str) -> Mineral | None:
    """Busca um mineral sem diferenciar maiusculas, espacos ou acentos."""

    return _MINERALS_BY_NAME.get(_normalize_name(name))
