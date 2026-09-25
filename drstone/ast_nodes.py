"""Nos da arvore sintatica abstrata (AST) da linguagem DrStone."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias


ScalarValue: TypeAlias = int | float | str


@dataclass(frozen=True)
class Literal:
    """Um valor literal numerico ou textual."""

    value: ScalarValue
    line: int
    column: int


@dataclass(frozen=True)
class Property:
    """Uma propriedade declarada dentro de um mineral."""

    name: str
    value: Literal
    line: int
    column: int


@dataclass(frozen=True)
class MineralDeclaration:
    """Declaracao de uma amostra mineral e suas propriedades."""

    name: str
    properties: list[Property]
    line: int
    column: int


@dataclass(frozen=True)
class IdentifyStatement:
    """Comando que solicita a identificacao de uma amostra."""

    name: str
    line: int
    column: int


Statement: TypeAlias = MineralDeclaration | IdentifyStatement


@dataclass(frozen=True)
class Program:
    """Raiz da AST de um programa DrStone."""

    statements: list[Statement]
