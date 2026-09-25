"""Testes do ponto de entrada do DrStone."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from drstone.main import execute_file, main


class MainTest(unittest.TestCase):
    def test_executes_example_file_through_complete_pipeline(self) -> None:
        output = execute_file(Path("examples/quartzo.stone"))

        self.assertIn("=== DrStone ===", output)
        self.assertIn("Analisando: pedra", output)
        self.assertIn("Mineral mais compatível:\nQuartzo", output)
        self.assertIn("Compatibilidade: 4/4", output)

    def test_cli_prints_result_and_returns_success(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            exit_code = main(["examples/quartzo.stone"])

        self.assertEqual(exit_code, 0)
        self.assertIn("Quartzo", stdout.getvalue())
        self.assertEqual(stderr.getvalue(), "")

    def test_reports_missing_file_without_traceback(self) -> None:
        stderr = io.StringIO()

        with redirect_stderr(stderr):
            exit_code = main(["examples/inexistente.stone"])

        self.assertEqual(exit_code, 1)
        self.assertIn("Erro de arquivo: arquivo não encontrado", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_reports_lexical_error(self) -> None:
        exit_code, message = self._run_invalid_source("@")

        self.assertEqual(exit_code, 1)
        self.assertIn("Erro léxico: Linha 1, coluna 1", message)

    def test_reports_syntax_error(self) -> None:
        source = """mineral pedra {
    dureza = 7
"""

        exit_code, message = self._run_invalid_source(source)

        self.assertEqual(exit_code, 1)
        self.assertIn("Erro sintático:", message)
        self.assertIn("esperado '}'", message)

    def test_reports_semantic_error(self) -> None:
        source = '''mineral pedra {
    dureza = "muito duro"
}'''

        exit_code, message = self._run_invalid_source(source)

        self.assertEqual(exit_code, 1)
        self.assertIn("Erro semântico:", message)
        self.assertIn("dureza deve ser numerica", message)

    @staticmethod
    def _run_invalid_source(source: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "programa.stone"
            path.write_text(source, encoding="utf-8")
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                exit_code = main([str(path)])
            return exit_code, stderr.getvalue()


if __name__ == "__main__":
    unittest.main()
