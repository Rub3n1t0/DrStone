"""Testes do analisador semantico do DrStone."""

import unittest

from drstone.lexer import tokenize
from drstone.parser import parse
from drstone.semantic import SemanticError, analyze


def analyze_source(source: str) -> None:
    analyze(parse(tokenize(source)))


class SemanticAnalyzerTest(unittest.TestCase):
    def test_rejects_unknown_property(self) -> None:
        source = """mineral pedra {
    origem = "Brasil"
}"""

        with self.assertRaisesRegex(SemanticError, "propriedade desconhecida"):
            analyze_source(source)

    def test_rejects_undeclared_mineral(self) -> None:
        with self.assertRaisesRegex(SemanticError, "nao foi declarado"):
            analyze_source("identificar quartzo")

    def test_rejects_duplicate_property(self) -> None:
        source = """mineral pedra {
    dureza = 7
    dureza = 8
}"""

        with self.assertRaisesRegex(SemanticError, "propriedade 'dureza' duplicada"):
            analyze_source(source)

    def test_rejects_hardness_with_wrong_type(self) -> None:
        source = '''mineral pedra {
    dureza = "muito duro"
}'''

        with self.assertRaisesRegex(SemanticError, "dureza deve ser numerica"):
            analyze_source(source)

    def test_rejects_hardness_outside_valid_range(self) -> None:
        for hardness in (0, 11):
            source = f"""mineral pedra {{
    dureza = {hardness}
}}"""

            with self.subTest(hardness=hardness):
                with self.assertRaisesRegex(SemanticError, "entre 1 e 10"):
                    analyze_source(source)

    def test_rejects_negative_density(self) -> None:
        source = """mineral pedra {
    densidade = -2.65
}"""

        with self.assertRaisesRegex(SemanticError, "nao pode ser negativa"):
            analyze_source(source)

    def test_rejects_density_with_wrong_type(self) -> None:
        source = '''mineral pedra {
    densidade = "alta"
}'''

        with self.assertRaisesRegex(SemanticError, "densidade deve ser numerica"):
            analyze_source(source)

    def test_rejects_text_property_with_wrong_type(self) -> None:
        for property_name in ("cor", "brilho"):
            source = f"""mineral pedra {{
    {property_name} = 7
}}"""

            with self.subTest(property_name=property_name):
                with self.assertRaisesRegex(SemanticError, "deve ser uma string"):
                    analyze_source(source)

    def test_rejects_duplicate_mineral_declaration(self) -> None:
        source = """mineral pedra {
    dureza = 7
}
mineral pedra {
    densidade = 2.65
}"""

        with self.assertRaisesRegex(SemanticError, "ja foi declarado"):
            analyze_source(source)

    def test_rejects_mineral_without_properties(self) -> None:
        source = """mineral pedra {
}"""

        with self.assertRaisesRegex(SemanticError, "ao menos uma propriedade"):
            analyze_source(source)

    def test_accepts_valid_program(self) -> None:
        source = '''mineral quartzo {
    cor = "incolor"
    dureza = 7
    densidade = 2.65
    brilho = "vitreo"
}

identificar quartzo'''

        program = parse(tokenize(source))

        self.assertIs(analyze(program), program)

    def test_reports_semantic_error_position(self) -> None:
        source = """mineral pedra {
    dureza = 20
}"""

        with self.assertRaises(SemanticError) as context:
            analyze_source(source)

        self.assertEqual((context.exception.line, context.exception.column), (2, 5))


if __name__ == "__main__":
    unittest.main()
