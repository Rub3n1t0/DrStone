"""Testes do analisador lexico do DrStone."""

import unittest

from drstone.lexer import LexerError, tokenize
from drstone.tokens import TokenType


class LexerTest(unittest.TestCase):
    def test_tokenizes_the_basic_example(self) -> None:
        tokens = tokenize("mineral amostra1 { dureza = 7 }")

        self.assertEqual(
            [token.type for token in tokens],
            [
                TokenType.MINERAL,
                TokenType.IDENTIFIER,
                TokenType.LBRACE,
                TokenType.DUREZA,
                TokenType.EQUALS,
                TokenType.NUMBER,
                TokenType.RBRACE,
                TokenType.EOF,
            ],
        )
        self.assertEqual(tokens[1].literal, "amostra1")
        self.assertEqual(tokens[5].literal, 7)

    def test_tokenizes_a_complete_program(self) -> None:
        source = '''mineral amostra1 {
cor = "incolor"
dureza = 7
densidade = 2.65
brilho = "vitreo"
}

identificar amostra1'''

        tokens = tokenize(source)
        types = [token.type for token in tokens]

        self.assertIn(TokenType.COR, types)
        self.assertIn(TokenType.DENSIDADE, types)
        self.assertIn(TokenType.BRILHO, types)
        self.assertIn(TokenType.IDENTIFICAR, types)
        self.assertEqual(
            [token.literal for token in tokens if token.type is TokenType.STRING],
            ["incolor", "vitreo"],
        )
        self.assertEqual(
            [token.literal for token in tokens if token.type is TokenType.NUMBER],
            [7, 2.65],
        )

    def test_preserves_newlines_and_ignores_comments(self) -> None:
        source = '# comentario inicial\ncor = "valor # textual" # final\n'
        tokens = tokenize(source)

        self.assertEqual(
            [token.type for token in tokens],
            [
                TokenType.NEWLINE,
                TokenType.COR,
                TokenType.EQUALS,
                TokenType.STRING,
                TokenType.NEWLINE,
                TokenType.EOF,
            ],
        )
        self.assertEqual(tokens[3].literal, "valor # textual")

    def test_decodes_supported_string_escapes(self) -> None:
        token = tokenize(r'"linha\n\t\"texto\"\\fim"')[0]

        self.assertIs(token.type, TokenType.STRING)
        self.assertEqual(token.literal, 'linha\n\t"texto"\\fim')

    def test_tokenizes_negative_number_for_semantic_validation(self) -> None:
        tokens = tokenize("densidade = -2.5")

        self.assertIs(tokens[2].type, TokenType.NUMBER)
        self.assertEqual(tokens[2].literal, -2.5)

    def test_reports_lexical_errors(self) -> None:
        invalid_cases = [
            ("dureza = +1", "caractere inesperado"),
            ('cor = "incolor', "string nao terminada"),
            (r'cor = "\x"', "sequencia de escape invalida"),
            ("cor = azul-claro", "caractere inesperado"),
        ]

        for source, message in invalid_cases:
            with self.subTest(source=source):
                with self.assertRaisesRegex(LexerError, message):
                    tokenize(source)

    def test_records_token_position(self) -> None:
        tokens = tokenize("mineral amostra1 {\n    dureza = 7\n}")
        dureza = next(token for token in tokens if token.type is TokenType.DUREZA)

        self.assertEqual((dureza.line, dureza.column), (2, 5))


if __name__ == "__main__":
    unittest.main()
