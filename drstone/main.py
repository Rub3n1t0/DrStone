"""Ponto de entrada de linha de comando do DrStone."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .interpreter import Interpreter
from .lexer import LexerError, tokenize
from .parser import ParserError, parse
from .semantic import SemanticError, analyze


def execute_file(file_path: str | Path) -> str:
    """Executa todas as etapas do DrStone para um arquivo fonte."""

    source = Path(file_path).read_text(encoding="utf-8")
    tokens = tokenize(source)
    program = parse(tokens)
    analyze(program)
    return Interpreter().execute(program, validate=False)


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m drstone.main",
        description="Executa um programa escrito na linguagem DrStone.",
    )
    parser.add_argument("arquivo", help="caminho para o arquivo .stone")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Executa a CLI e devolve um codigo de saida para o sistema operacional."""

    arguments = _argument_parser().parse_args(argv)
    file_path = Path(arguments.arquivo)

    try:
        output = execute_file(file_path)
    except FileNotFoundError:
        print(f"Erro de arquivo: arquivo não encontrado: {file_path}", file=sys.stderr)
        return 1
    except IsADirectoryError:
        print(f"Erro de arquivo: o caminho é um diretório: {file_path}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"Erro de arquivo: sem permissão para ler: {file_path}", file=sys.stderr)
        return 1
    except UnicodeDecodeError:
        print(
            f"Erro de codificação: {file_path} deve estar em UTF-8.",
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
        print(f"Erro de arquivo: não foi possível ler {file_path}: {error}", file=sys.stderr)
        return 1

    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
