"""Ponto de entrada de linha de comando do DrStone."""

from __future__ import annotations

import argparse
import math
import sys
from collections.abc import Sequence
from pathlib import Path

from .interpreter import Interpreter
from .lexer import LexerError, tokenize
from .parser import ParserError, parse
from .semantic import SemanticError, analyze


def execute_source(source: str) -> str:
    """Executa todas as etapas do DrStone para um codigo-fonte."""

    tokens = tokenize(source)
    program = parse(tokens)
    analyze(program)
    return Interpreter().execute(program, validate=False)


def execute_file(file_path: str | Path) -> str:
    """Executa todas as etapas do DrStone para um arquivo fonte."""

    source = Path(file_path).read_text(encoding="utf-8")
    return execute_source(source)


def _finite_number(value: str) -> float:
    """Converte um argumento numerico e rejeita infinito e NaN."""

    try:
        number = float(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(f"valor numerico invalido: {value}") from error
    if not math.isfinite(number):
        raise argparse.ArgumentTypeError("o valor deve ser um numero finito")
    return number


def _quote_string(value: str) -> str:
    """Converte texto da CLI em um literal string valido em DrStone."""

    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    return f'"{escaped}"'


def _source_from_arguments(arguments: argparse.Namespace) -> str:
    properties = (
        ("cor", arguments.cor, _quote_string),
        ("dureza", arguments.dureza, lambda value: format(value, "g")),
        ("densidade", arguments.densidade, lambda value: format(value, "g")),
        ("brilho", arguments.brilho, _quote_string),
    )
    lines = [f"mineral {arguments.nome} {{"]
    lines.extend(
        f"    {name} = {formatter(value)}"
        for name, value, formatter in properties
        if value is not None
    )
    lines.extend(("}", "", f"identificar {arguments.nome}"))
    return "\n".join(lines)


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m drstone.main",
        description="Executa um programa escrito na linguagem DrStone.",
    )
    parser.add_argument("arquivo", nargs="?", help="caminho para o arquivo .stone")
    parser.add_argument(
        "--nome",
        default="amostra",
        help="nome da amostra no modo direto (padrao: amostra)",
    )
    parser.add_argument("--dureza", type=_finite_number, help="dureza na escala Mohs")
    parser.add_argument("--densidade", type=_finite_number, help="densidade da amostra")
    parser.add_argument("--cor", help="cor observada")
    parser.add_argument("--brilho", help="tipo de brilho observado")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Executa a CLI e devolve um codigo de saida para o sistema operacional."""

    argument_parser = _argument_parser()
    arguments = argument_parser.parse_args(argv)
    direct_values = (
        arguments.cor,
        arguments.dureza,
        arguments.densidade,
        arguments.brilho,
    )

    if arguments.arquivo and any(value is not None for value in direct_values):
        print(
            "Erro de argumentos: use um arquivo .stone ou propriedades diretas, não ambos.",
            file=sys.stderr,
        )
        return 2
    if not arguments.arquivo and all(value is None for value in direct_values):
        argument_parser.print_usage(sys.stderr)
        print(
            "Erro de argumentos: informe um arquivo .stone ou ao menos uma propriedade.",
            file=sys.stderr,
        )
        return 2

    try:
        if arguments.arquivo:
            output = execute_file(Path(arguments.arquivo))
        else:
            output = execute_source(_source_from_arguments(arguments))
    except FileNotFoundError:
        print(
            f"Erro de arquivo: arquivo não encontrado: {arguments.arquivo}",
            file=sys.stderr,
        )
        return 1
    except IsADirectoryError:
        print(
            f"Erro de arquivo: o caminho é um diretório: {arguments.arquivo}",
            file=sys.stderr,
        )
        return 1
    except PermissionError:
        print(
            f"Erro de arquivo: sem permissão para ler: {arguments.arquivo}",
            file=sys.stderr,
        )
        return 1
    except UnicodeDecodeError:
        print(
            f"Erro de codificação: {arguments.arquivo} deve estar em UTF-8.",
            file=sys.stderr,
        )
        return 1
    except LexerError as error:
        print(f"Erro léxico: {error}", file=sys.stderr)
        return 1
    except ParserError as error:
        print(f"Erro sintático: {error}", file=sys.stderr)
        return 1
    except SemanticError as error:
        print(f"Erro semântico: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(
            f"Erro de arquivo: não foi possível ler {arguments.arquivo}: {error}",
            file=sys.stderr,
        )
        return 1

    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
