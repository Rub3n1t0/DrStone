"""Analisador lexico manual da linguagem DrStone."""

from .tokens import Token, TokenType


class LexerError(ValueError):
    """Erro encontrado durante a analise lexica."""

    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"Linha {line}, coluna {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    """Percorre o codigo-fonte e o converte em uma lista de tokens."""

    _KEYWORDS = {
        "mineral": TokenType.MINERAL,
        "identificar": TokenType.IDENTIFICAR,
        "cor": TokenType.COR,
        "dureza": TokenType.DUREZA,
        "densidade": TokenType.DENSIDADE,
        "brilho": TokenType.BRILHO,
    }

    _SINGLE_CHARACTER_TOKENS = {
        "=": TokenType.EQUALS,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
    }

    _ESCAPES = {
        '"': '"',
        "\\": "\\",
        "n": "\n",
        "t": "\t",
    }

    def __init__(self, source: str) -> None:
        # Internamente, toda quebra de linha tem um unico formato.
        self.source = source.replace("\r\n", "\n").replace("\r", "\n")
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1
        self.tokens: list[Token] = []

    def tokenize(self) -> list[Token]:
        """Analisa todo o codigo-fonte e devolve os tokens, incluindo EOF."""

        while not self._is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        character = self._advance()

        if character in " \t":
            return

        if character == "\n":
            self._add_token(TokenType.NEWLINE)
            return

        if character == "#":
            self._skip_comment()
            return

        token_type = self._SINGLE_CHARACTER_TOKENS.get(character)
        if token_type is not None:
            self._add_token(token_type)
            return

        if character == '"':
            self._scan_string()
            return

        if character.isascii() and character.isdigit():
            self._scan_number()
            return

        if character == "-" and self._peek().isascii() and self._peek().isdigit():
            self._scan_number()
            return

        if self._is_identifier_start(character):
            self._scan_identifier()
            return

        raise LexerError(
            f"caractere inesperado {character!r}",
            self.start_line,
            self.start_column,
        )

    def _scan_identifier(self) -> None:
        while self._is_identifier_part(self._peek()):
            self._advance()

        lexeme = self.source[self.start : self.current]
        token_type = self._KEYWORDS.get(lexeme, TokenType.IDENTIFIER)
        literal = lexeme if token_type is TokenType.IDENTIFIER else None
        self._add_token(token_type, literal)

    def _scan_number(self) -> None:
        while self._peek().isascii() and self._peek().isdigit():
            self._advance()

        if (
            self._peek() == "."
            and self._peek_next().isascii()
            and self._peek_next().isdigit()
        ):
            self._advance()
            while self._peek().isascii() and self._peek().isdigit():
                self._advance()

        lexeme = self.source[self.start : self.current]
        literal = float(lexeme) if "." in lexeme else int(lexeme)
        self._add_token(TokenType.NUMBER, literal)

    def _scan_string(self) -> None:
        value: list[str] = []

        while not self._is_at_end():
            character = self._advance()

            if character == '"':
                self._add_token(TokenType.STRING, "".join(value))
                return

            if character == "\n":
                raise LexerError(
                    "string nao terminada antes do fim da linha",
                    self.start_line,
                    self.start_column,
                )

            if character == "\\":
                if self._is_at_end():
                    break
                escape_column = self.column - 1
                escaped = self._advance()
                replacement = self._ESCAPES.get(escaped)
                if replacement is None:
                    raise LexerError(
                        f"sequencia de escape invalida \\{escaped}",
                        self.line,
                        escape_column,
                    )
                value.append(replacement)
                continue

            value.append(character)

        raise LexerError(
            "string nao terminada",
            self.start_line,
            self.start_column,
        )

    def _skip_comment(self) -> None:
        while self._peek() not in {"\n", "\0"}:
            self._advance()

    def _add_token(self, token_type: TokenType, literal: object = None) -> None:
        lexeme = self.source[self.start : self.current]
        self.tokens.append(
            Token(
                token_type,
                lexeme,
                literal,
                self.start_line,
                self.start_column,
            )
        )

    def _advance(self) -> str:
        character = self.source[self.current]
        self.current += 1
        if character == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return character

    def _peek(self) -> str:
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    @staticmethod
    def _is_identifier_start(character: str) -> bool:
        return character.isascii() and (character.isalpha() or character == "_")

    @staticmethod
    def _is_identifier_part(character: str) -> bool:
        return character.isascii() and (character.isalnum() or character == "_")


def tokenize(source: str) -> list[Token]:
    """Atalho funcional para analisar um trecho de codigo DrStone."""

    return Lexer(source).tokenize()
