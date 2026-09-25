"""Parser recursivo descendente da linguagem DrStone."""

from collections.abc import Sequence

from .ast_nodes import (
    IdentifyStatement,
    Literal,
    MineralDeclaration,
    Program,
    Property,
    Statement,
)
from .tokens import Token, TokenType


class ParserError(ValueError):
    """Erro encontrado durante a analise sintatica."""

    def __init__(self, token: Token, message: str) -> None:
        super().__init__(f"Linha {token.line}, coluna {token.column}: {message}")
        self.token = token
        self.line = token.line
        self.column = token.column


class Parser:
    """Consome tokens DrStone e constroi uma AST."""

    _PROPERTY_TYPES = {
        TokenType.COR,
        TokenType.DUREZA,
        TokenType.DENSIDADE,
        TokenType.BRILHO,
        TokenType.IDENTIFIER,
    }

    def __init__(self, tokens: Sequence[Token]) -> None:
        if not tokens or tokens[-1].type is not TokenType.EOF:
            raise ValueError("A sequencia de tokens deve terminar com EOF.")
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        """Analisa todos os comandos ate encontrar EOF."""

        statements: list[Statement] = []
        self._skip_newlines()

        while not self._is_at_end():
            statements.append(self._statement())
            self._consume_statement_end()

        return Program(statements)

    def _statement(self) -> Statement:
        if self._match(TokenType.MINERAL):
            return self._mineral_declaration(self._previous())
        if self._match(TokenType.IDENTIFICAR):
            return self._identify_statement(self._previous())

        raise self._error(
            self._peek(),
            "esperado 'mineral' ou 'identificar' no inicio do comando",
        )

    def _mineral_declaration(self, keyword: Token) -> MineralDeclaration:
        name = self._consume(
            TokenType.IDENTIFIER,
            "esperado o nome do mineral depois de 'mineral'",
        )
        self._consume(
            TokenType.LBRACE,
            "esperado '{' depois do nome do mineral",
        )
        self._consume(
            TokenType.NEWLINE,
            "esperada uma quebra de linha depois de '{'",
        )
        self._skip_newlines()

        properties: list[Property] = []
        while not self._check(TokenType.RBRACE):
            if self._is_at_end():
                raise self._error(
                    self._peek(),
                    "esperado '}' para fechar a declaracao do mineral",
                )

            properties.append(self._property())
            self._consume(
                TokenType.NEWLINE,
                "esperada uma quebra de linha depois da propriedade",
            )
            self._skip_newlines()

        self._advance()
        return MineralDeclaration(
            name=name.lexeme,
            properties=properties,
            line=keyword.line,
            column=keyword.column,
        )

    def _property(self) -> Property:
        name = self._peek()
        if name.type not in self._PROPERTY_TYPES:
            raise self._error(name, "esperado o nome de uma propriedade")
        self._advance()

        self._consume(
            TokenType.EQUALS,
            "esperado '=' depois do nome da propriedade",
        )
        value_token = self._peek()
        if not self._match(TokenType.NUMBER, TokenType.STRING):
            raise self._error(value_token, "esperado um numero ou uma string")

        literal = Literal(
            value=value_token.literal,
            line=value_token.line,
            column=value_token.column,
        )
        return Property(
            name=name.lexeme,
            value=literal,
            line=name.line,
            column=name.column,
        )

    def _identify_statement(self, keyword: Token) -> IdentifyStatement:
        name = self._consume(
            TokenType.IDENTIFIER,
            "esperado o nome do mineral depois de 'identificar'",
        )
        return IdentifyStatement(
            name=name.lexeme,
            line=keyword.line,
            column=keyword.column,
        )

    def _consume_statement_end(self) -> None:
        if self._match(TokenType.NEWLINE):
            self._skip_newlines()
            return
        if not self._is_at_end():
            raise self._error(
                self._peek(),
                "esperada uma quebra de linha depois do comando",
            )

    def _skip_newlines(self) -> None:
        while self._match(TokenType.NEWLINE):
            pass

    def _match(self, *types: TokenType) -> bool:
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type is token_type

    def _advance(self) -> Token:
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        return self._peek().type is TokenType.EOF

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    @staticmethod
    def _error(token: Token, message: str) -> ParserError:
        return ParserError(token, message)


def parse(tokens: Sequence[Token]) -> Program:
    """Atalho funcional para construir a AST de uma sequencia de tokens."""

    return Parser(tokens).parse()
