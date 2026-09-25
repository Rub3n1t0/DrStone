"""Interpretador da linguagem DrStone."""

from dataclasses import dataclass
from unicodedata import combining, normalize

from .ast_nodes import IdentifyStatement, MineralDeclaration, Program, ScalarValue
from .minerals import MINERALS, Mineral
from .semantic import analyze


@dataclass(frozen=True)
class CriterionMatch:
    """Um criterio da amostra que coincide com um mineral conhecido."""

    property_name: str
    description: str


@dataclass(frozen=True)
class MineralCompatibility:
    """Resultado da comparacao entre uma amostra e um mineral."""

    mineral: Mineral
    matching_criteria: tuple[CriterionMatch, ...]
    total_criteria: int

    @property
    def score(self) -> int:
        return len(self.matching_criteria)


@dataclass(frozen=True)
class IdentificationResult:
    """Resultado completo de um comando identificar."""

    sample_name: str
    properties: dict[str, ScalarValue]
    compatible_minerals: tuple[MineralCompatibility, ...]

    @property
    def best_match(self) -> MineralCompatibility | None:
        if not self.compatible_minerals:
            return None
        return self.compatible_minerals[0]


class Interpreter:
    """Executa declaracoes e comandos de identificacao da AST."""

    _PROPERTY_LABELS = {
        "cor": "Cor",
        "dureza": "Dureza",
        "densidade": "Densidade",
        "brilho": "Brilho",
    }

    def __init__(self) -> None:
        self.samples: dict[str, dict[str, ScalarValue]] = {}
        self.identifications: list[IdentificationResult] = []

    def execute(self, program: Program, *, validate: bool = True) -> str:
        """Executa um programa e devolve sua saida textual.

        Por padrao, a AST e validada antes da execucao. O ponto de entrada pode
        desativar essa etapa quando ja tiver executado a analise semantica.
        """

        if validate:
            analyze(program)
        self.samples.clear()
        self.identifications.clear()

        for statement in program.statements:
            if isinstance(statement, MineralDeclaration):
                self.samples[statement.name] = {
                    item.name: item.value.value for item in statement.properties
                }
            elif isinstance(statement, IdentifyStatement):
                properties = self.samples[statement.name]
                self.identifications.append(
                    self._identify(statement.name, properties)
                )

        return "\n\n".join(
            self._format_identification(result) for result in self.identifications
        )

    def _identify(
        self,
        sample_name: str,
        properties: dict[str, ScalarValue],
    ) -> IdentificationResult:
        compatibilities: list[MineralCompatibility] = []

        for mineral in MINERALS:
            criteria = tuple(
                criterion
                for name, value in properties.items()
                if (criterion := self._compare_property(name, value, mineral))
                is not None
            )
            if criteria:
                compatibilities.append(
                    MineralCompatibility(
                        mineral=mineral,
                        matching_criteria=criteria,
                        total_criteria=len(properties),
                    )
                )

        # A ordenacao e estavel; empates preservam a ordem didatica do catalogo.
        compatibilities.sort(key=lambda item: item.score, reverse=True)
        return IdentificationResult(
            sample_name=sample_name,
            properties=dict(properties),
            compatible_minerals=tuple(compatibilities),
        )

    def _compare_property(
        self,
        name: str,
        value: ScalarValue,
        mineral: Mineral,
    ) -> CriterionMatch | None:
        if name == "dureza" and mineral.dureza_min <= value <= mineral.dureza_max:
            return CriterionMatch(
                name,
                f"Dureza {self._format_number(value)} dentro da faixa "
                f"{self._format_range(mineral.dureza_min, mineral.dureza_max)}",
            )

        if (
            name == "densidade"
            and mineral.densidade_min <= value <= mineral.densidade_max
        ):
            return CriterionMatch(
                name,
                f"Densidade {self._format_number(value)} dentro da faixa "
                f"{self._format_range(mineral.densidade_min, mineral.densidade_max)}",
            )

        if name == "cor" and self._text_matches(str(value), mineral.cor, "variada"):
            return CriterionMatch(name, f"Cor compatível: {value}")

        if name == "brilho" and self._text_matches(str(value), mineral.brilho):
            return CriterionMatch(name, f"Brilho compatível: {value}")

        return None

    def _format_identification(self, result: IdentificationResult) -> str:
        lines = ["=== DrStone ===", "", f"Analisando: {result.sample_name}", ""]

        for name, value in result.properties.items():
            label = self._PROPERTY_LABELS.get(name, name.capitalize())
            lines.append(f"{label}: {value}")

        lines.extend(["", "Mineral mais compatível:"])
        best_match = result.best_match
        if best_match is None:
            lines.append("Nenhum mineral compatível encontrado.")
            return "\n".join(lines)

        lines.extend(
            [
                best_match.mineral.nome,
                "",
                f"Compatibilidade: {best_match.score}/{best_match.total_criteria}",
                "Critérios coincidentes:",
            ]
        )
        lines.extend(
            f"- {criterion.description}"
            for criterion in best_match.matching_criteria
        )
        return "\n".join(lines)

    @staticmethod
    def _text_matches(value: str, reference: str, wildcard: str | None = None) -> bool:
        normalized_value = Interpreter._normalize_text(value)
        normalized_reference = Interpreter._normalize_text(reference)
        return normalized_value in normalized_reference or (
            wildcard is not None
            and Interpreter._normalize_text(wildcard) in normalized_reference
        )

    @staticmethod
    def _normalize_text(value: str) -> str:
        decomposed = normalize("NFKD", value.strip().casefold())
        return "".join(character for character in decomposed if not combining(character))

    @staticmethod
    def _format_number(value: int | float) -> str:
        return f"{value:g}"

    @staticmethod
    def _format_range(minimum: float, maximum: float) -> str:
        if minimum == maximum:
            return f"{minimum:g}"
        return f"{minimum:g}-{maximum:g}"


def interpret(program: Program) -> str:
    """Atalho funcional para executar uma AST DrStone."""

    return Interpreter().execute(program)
