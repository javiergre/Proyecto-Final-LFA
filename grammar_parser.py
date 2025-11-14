import re

class GrammarParser:
    """
    Parser sencillo para gramáticas de Chomsky.

    Formato esperado de cada producción (se permiten espacios opcionales):

        S -> aSB | ab
        A→0A|1

    - Se aceptan tanto "->" como "→".
    - Se ignoran líneas en blanco y líneas que empiezan con "#" o "//".
    - Lado izquierdo: una o más letras / dígitos / guiones bajos.
    - Lado derecho: una o varias alternativas separadas por "|".
    - La producción vacía puede escribirse como: ε, lambda, λ o "" (cadena vacía).
    """

    def __init__(self):
        # Coincide con LHS -> RHS o LHS → RHS
        self.production_pattern = re.compile(
            r'^\s*([A-Za-z][A-Za-z0-9_]*)\s*(?:->|→)\s*(.+)\s*$'
        )

    def parse_grammar(self, grammar_text):
        """
        Parsea el texto de gramática y devuelve un diccionario:

            { "S": ["aSB", "ab"], "B": ["b"] }

        Si no se reconoce ninguna producción válida, devuelve {} para que
        el resto del programa pueda interpretar la entrada como autómata.
        """
        productions = {}
        lines = grammar_text.splitlines()

        for line in lines:
            stripped = line.strip()
            # Ignorar comentarios o líneas vacías
            if not stripped or stripped.startswith("#") or stripped.startswith("//"):
                continue

            m = self.production_pattern.match(stripped)
            if not m:
                continue

            lhs = m.group(1)
            rhs_part = m.group(2)

            alternatives = [alt.strip() for alt in rhs_part.split("|")]

            for alt in alternatives:
                if alt in ("ε", "lambda", "λ"):
                    rhs = ""  # representamos epsilon como cadena vacía
                else:
                    rhs = alt

                productions.setdefault(lhs, []).append(rhs)

        return productions

    def validate_grammar(self, productions):
        """
        Valida la estructura básica de una gramática.
        Devuelve (errores, advertencias).
        """
        errors = []
        warnings = []

        if not productions:
            errors.append("La gramática está vacía o no se reconoció ninguna producción.")
            return errors, warnings

        for lhs, rhs_list in productions.items():
            if not lhs:
                errors.append("Se encontró un lado izquierdo vacío.")
                continue

            if not rhs_list:
                warnings.append(f"La variable '{lhs}' no tiene producciones.")
                continue

            # LHS debe ser un identificador alfanumérico
            if not lhs[0].isalpha():
                errors.append(f"El lado izquierdo '{lhs}' debe iniciar con una letra.")
            if not all(c.isalnum() or c == "_" for c in lhs):
                errors.append(f"El lado izquierdo '{lhs}' contiene caracteres inválidos.")

            # RHS puede ser cadena vacía (epsilon) o combinación de símbolos
            for rhs in rhs_list:
                if rhs == "":
                    # epsilon: permitido
                    continue
                if any(c.isspace() for c in rhs):
                    warnings.append(
                        f"La producción '{lhs} -> {rhs}' contiene espacios internos; "
                        "esto puede causar ambigüedad en la interpretación."
                    )

        return errors, warnings
