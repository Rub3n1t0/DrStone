"""Analisador semantico da linguagem DrStone."""

from .ast_nodes import (
    IdentifyStatement,
    MineralDeclaration,
    Program,
    Property,
)


class SemanticError(ValueError):
    """Erro encontrado durante a analise semantica."""

    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(f"Linha {line}, coluna {column}: {message}")
        self.line = line
        self.column = column


class SemanticAnalyzer:
    """Valida nomes, propriedades, tipos e limites dos minerais."""

    _KNOWN_PROPERTIES = {"cor", "dureza", "densidade", "brilho"}
    _TEXT_PROPERTIES = {"cor", "brilho"}
    _NUMERIC_PROPERTIES = {"dureza", "densidade"}

    def __init__(self) -> None:
        self.declared_minerals: dict[str, MineralDeclaration] = {}

    def analyze(self, program: Program) -> Program:
        """Valida um programa e devolve a AST quando nao ha erros."""

        self.declared_minerals.clear()

        for statement in program.statements:
            if isinstance(statement, MineralDeclaration):
                self._analyze_mineral(statement)
            elif isinstance(statement, IdentifyStatement):
                self._analyze_identify(statement)

        return program

    def _analyze_mineral(self, declaration: MineralDeclaration) -> None:
        if declaration.name in self.declared_minerals:
            self._raise_error(
                declaration,
                f"mineral '{declaration.name}' ja foi declarado",
            )

        if not declaration.properties:
            self._raise_error(
                declaration,
                f"mineral '{declaration.name}' deve possuir ao menos uma propriedade",
            )

        property_names: set[str] = set()
        for property_node in declaration.properties:
            if property_node.name in property_names:
                self._raise_error(
                    property_node,
                    f"propriedade '{property_node.name}' duplicada",
                )
            property_names.add(property_node.name)

            if property_node.name not in self._KNOWN_PROPERTIES:
                self._raise_error(
                    property_node,
                    f"propriedade desconhecida: '{property_node.name}'",
                )

            self._validate_property(property_node)

        self.declared_minerals[declaration.name] = declaration

    def _analyze_identify(self, statement: IdentifyStatement) -> None:
        if statement.name not in self.declared_minerals:
            self._raise_error(
                statement,
                f"mineral '{statement.name}' nao foi declarado",
            )

    def _validate_property(self, property_node: Property) -> None:
        name = property_node.name
        value = property_node.value.value

        if name in self._TEXT_PROPERTIES:
            if not isinstance(value, str):
                self._raise_error(property_node, f"{name} deve ser uma string")
            return

        if name in self._NUMERIC_PROPERTIES and not self._is_number(value):
            self._raise_error(property_node, f"{name} deve ser numerica")

        if name == "dureza" and not 1 <= value <= 10:
            self._raise_error(property_node, "dureza deve estar entre 1 e 10")

        if name == "densidade" and value < 0:
            self._raise_error(property_node, "densidade nao pode ser negativa")

    @staticmethod
    def _is_number(value: object) -> bool:
        return isinstance(value, (int, float)) and not isinstance(value, bool)

    @staticmethod
    def _raise_error(node: object, message: str) -> None:
        line = getattr(node, "line")
        column = getattr(node, "column")
        raise SemanticError(message, line, column)


def analyze(program: Program) -> Program:
    """Atalho funcional para analisar semanticamente uma AST."""

    return SemanticAnalyzer().analyze(program)
