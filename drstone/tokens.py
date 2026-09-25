"""Tipos de token produzidos pelo analisador lexico do DrStone."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any


class TokenType(Enum):
    """Categorias lexicas reconhecidas pela versao inicial da linguagem."""

    # Palavras reservadas
    MINERAL = auto()
    IDENTIFICAR = auto()

    # Propriedades basicas do dominio
    COR = auto()
    DUREZA = auto()
    DENSIDADE = auto()
    BRILHO = auto()

    # Literais e nomes
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()

    # Operadores e delimitadores
    EQUALS = auto()
    LBRACE = auto()
    RBRACE = auto()
    NEWLINE = auto()

    EOF = auto()


@dataclass(frozen=True)
class Token:
    """Um token e seu local de origem no codigo-fonte."""

    type: TokenType
    lexeme: str
    literal: Any
    line: int
    column: int

    def __str__(self) -> str:
        if self.literal is None:
            return self.type.name
        return f"{self.type.name}({self.literal})"
