"""Testes da execucao de programas DrStone."""

import unittest

from drstone.interpreter import Interpreter, interpret
from drstone.lexer import tokenize
from drstone.parser import parse


def parse_source(source: str):
    return parse(tokenize(source))


class InterpreterTest(unittest.TestCase):
    def test_identifies_quartz_as_the_best_match(self) -> None:
        source = '''mineral pedra {
    dureza = 7
    densidade = 2.65
    brilho = "vitreo"
}

identificar pedra'''
        interpreter = Interpreter()

        output = interpreter.execute(parse_source(source))
        result = interpreter.identifications[0]

        self.assertEqual(result.best_match.mineral.nome, "Quartzo")
        self.assertEqual(result.best_match.score, 3)
        self.assertEqual(
            [item.property_name for item in result.best_match.matching_criteria],
            ["dureza", "densidade", "brilho"],
        )
        self.assertIn("=== DrStone ===", output)
        self.assertIn("Analisando: pedra", output)
        self.assertIn("Dureza: 7", output)
        self.assertIn("Densidade: 2.65", output)
        self.assertIn("Brilho: vitreo", output)
        self.assertIn("Mineral mais compatível:\nQuartzo", output)
        self.assertIn("Compatibilidade: 3/3", output)
        self.assertIn("Critérios coincidentes:", output)

    def test_keeps_compatible_minerals_ordered_by_score(self) -> None:
        source = '''mineral pedra {
    dureza = 7
    densidade = 2.65
}

identificar pedra'''
        interpreter = Interpreter()

        interpreter.execute(parse_source(source))
        matches = interpreter.identifications[0].compatible_minerals

        self.assertEqual(matches[0].mineral.nome, "Quartzo")
        self.assertEqual(matches[0].score, 2)
        self.assertTrue(all(matches[index].score >= matches[index + 1].score
                            for index in range(len(matches) - 1)))

    def test_reports_when_no_criterion_matches(self) -> None:
        source = '''mineral pedra {
    brilho = "fosco"
}

identificar pedra'''

        output = interpret(parse_source(source))

        self.assertIn("Nenhum mineral compatível encontrado.", output)

    def test_identifies_a_variety_imported_from_the_spreadsheet(self) -> None:
        source = '''mineral pedra {
    dureza = 9
    densidade = 4.0
    cor = "vermelho"
    brilho = "vitreo"
}

identificar pedra'''
        interpreter = Interpreter()

        interpreter.execute(parse_source(source))
        best_match = interpreter.identifications[0].best_match

        self.assertEqual(best_match.mineral.nome, "Rubi")
        self.assertEqual(best_match.score, 4)

    def test_matches_text_ignoring_case_and_accents(self) -> None:
        source = '''mineral pedra {
    dureza = 7
    brilho = "VÍTREO"
}

identificar pedra'''
        interpreter = Interpreter()

        interpreter.execute(parse_source(source))
        best_match = interpreter.identifications[0].best_match

        self.assertEqual(best_match.mineral.nome, "Quartzo")
        self.assertEqual(best_match.score, 2)

    def test_executes_multiple_identify_commands(self) -> None:
        source = '''mineral pedra1 {
    dureza = 1
}
mineral pedra2 {
    dureza = 10
}
identificar pedra1
identificar pedra2'''
        interpreter = Interpreter()

        output = interpreter.execute(parse_source(source))

        self.assertEqual(
            [result.best_match.mineral.nome for result in interpreter.identifications],
            ["Talco", "Diamante"],
        )
        self.assertEqual(output.count("=== DrStone ==="), 2)


if __name__ == "__main__":
    unittest.main()
