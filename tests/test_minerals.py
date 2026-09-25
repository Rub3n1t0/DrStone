"""Testes da base didatica de minerais do DrStone."""

import unittest
from dataclasses import FrozenInstanceError

from drstone.minerals import MINERALS, Mineral, get_mineral


class MineralsTest(unittest.TestCase):
    def test_contains_the_spreadsheet_database_and_legacy_entries(self) -> None:
        names = {mineral.nome for mineral in MINERALS}

        self.assertEqual(len(MINERALS), 106)
        self.assertEqual(len(names), 106)
        self.assertTrue(
            {
                "Quartzo",
                "Talco",
                "Gipsita",
                "Feldspato",
                "Topázio",
                "Coríndon",
                "Diamante",
                "Rubi",
                "Safira azul",
                "Benitoíta",
            }.issubset(names)
        )

    def test_preserves_representative_spreadsheet_values(self) -> None:
        ruby = get_mineral("rubi")
        benitoite = get_mineral("benitoita")

        self.assertEqual(
            (ruby.dureza_min, ruby.dureza_max, ruby.densidade_min, ruby.densidade_max),
            (9.0, 9.0, 3.97, 4.05),
        )
        self.assertEqual(ruby.cor, "vermelho; vermelho-púrpura")
        self.assertEqual(benitoite.brilho, "vítreo a adamantino")

    def test_each_mineral_has_valid_didactic_ranges(self) -> None:
        for mineral in MINERALS:
            with self.subTest(mineral=mineral.nome):
                self.assertLessEqual(mineral.dureza_min, mineral.dureza_max)
                self.assertLessEqual(mineral.densidade_min, mineral.densidade_max)
                self.assertGreaterEqual(mineral.dureza_min, 1)
                self.assertLessEqual(mineral.dureza_max, 10)
                self.assertGreater(mineral.densidade_min, 0)
                self.assertTrue(mineral.cor)
                self.assertTrue(mineral.brilho)

    def test_finds_mineral_ignoring_case_accents_and_spaces(self) -> None:
        self.assertEqual(get_mineral(" quartzo ").nome, "Quartzo")
        self.assertEqual(get_mineral("TOPAZIO").nome, "Topázio")
        self.assertEqual(get_mineral("corindon").nome, "Coríndon")

    def test_returns_none_for_unknown_mineral(self) -> None:
        self.assertIsNone(get_mineral("mineral inexistente"))

    def test_mineral_records_are_immutable(self) -> None:
        mineral = get_mineral("diamante")

        self.assertIsInstance(mineral, Mineral)
        with self.assertRaises(FrozenInstanceError):
            mineral.dureza_max = 11


if __name__ == "__main__":
    unittest.main()
