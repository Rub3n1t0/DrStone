"""Testes do parser e da construcao da AST do DrStone."""

import unittest

from drstone.ast_nodes import IdentifyStatement, MineralDeclaration
from drstone.lexer import tokenize
from drstone.parser import ParserError, parse


class ParserTest(unittest.TestCase):
    def test_builds_mineral_declaration_ast(self) -> None:
        source = """mineral quartzo {
    dureza = 7
    densidade = 2.65
}"""

        program = parse(tokenize(source))

        self.assertEqual(len(program.statements), 1)
        declaration = program.statements[0]
        self.assertIsInstance(declaration, MineralDeclaration)
        self.assertEqual(declaration.name, "quartzo")
        self.assertEqual(
            [(item.name, item.value.value) for item in declaration.properties],
            [("dureza", 7), ("densidade", 2.65)],
        )

    def test_builds_complete_program_ast(self) -> None:
        source = '''
# Uma linha de comentario
mineral quartzo {
    cor = "incolor"
    dureza = 7
}

identificar quartzo
'''

        program = parse(tokenize(source))

        self.assertEqual(len(program.statements), 2)
        declaration, identify = program.statements
        self.assertIsInstance(declaration, MineralDeclaration)
        self.assertEqual(declaration.properties[0].value.value, "incolor")
        self.assertIsInstance(identify, IdentifyStatement)
        self.assertEqual(identify.name, "quartzo")

    def test_accepts_generic_property_names(self) -> None:
        source = """mineral amostra1 {
    origem = "Brasil"
}"""

        declaration = parse(tokenize(source)).statements[0]

        self.assertIsInstance(declaration, MineralDeclaration)
        self.assertEqual(declaration.properties[0].name, "origem")

    def test_accepts_an_empty_program(self) -> None:
        program = parse(tokenize("\n# somente comentario\n"))

        self.assertEqual(program.statements, [])

    def test_reports_syntax_errors(self) -> None:
        invalid_cases = [
            (
                "mineral {\n}",
                "esperado o nome do mineral",
            ),
            (
                "mineral quartzo {\n    dureza 7\n}",
                "esperado '='",
            ),
            (
                "mineral quartzo {\n    dureza = alta\n}",
                "esperado um numero ou uma string",
            ),
            (
                "mineral quartzo {\n    dureza = 7\n",
                "esperado '}'",
            ),
            (
                "identificar",
                "esperado o nome do mineral",
            ),
            (
                "quartzo",
                "esperado 'mineral' ou 'identificar'",
            ),
        ]

        for source, message in invalid_cases:
            with self.subTest(source=source):
                with self.assertRaisesRegex(ParserError, message):
                    parse(tokenize(source))

    def test_reports_error_position(self) -> None:
        source = """mineral quartzo {
    dureza 7
}"""

        with self.assertRaises(ParserError) as context:
            parse(tokenize(source))

        self.assertEqual((context.exception.line, context.exception.column), (2, 12))

    def test_requires_line_breaks_inside_a_mineral(self) -> None:
        source = "mineral quartzo { dureza = 7 }"

        with self.assertRaisesRegex(ParserError, "quebra de linha depois de"):
            parse(tokenize(source))


if __name__ == "__main__":
    unittest.main()
