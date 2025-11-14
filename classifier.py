import re

class ChomskyClassifier:
    
    def __init__(self):
        self.type_descriptions = {
            "Tipo 3": "Gramática Regular",
            "Tipo 2": "Gramática Libre de Contexto",
            "Tipo 1": "Gramática Sensible al Contexto",
            "Tipo 0": "Gramática Recursivamente Enumerable",
        }

    # ------------------------------------------------------------------
    # API principal
    # ------------------------------------------------------------------
    def classify(self, productions):
        steps = []
        steps.append("🔍 Iniciando análisis de la gramática.")
        steps.append("Producciones detectadas:")

        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                rhs_str = rhs if rhs != "" else "ε"
                steps.append(f"  {lhs} → {rhs_str}")

        # Comprobación jerárquica: 3 ⊂ 2 ⊂ 1 ⊂ 0
        steps.append("\nPaso 1: ¿La gramática es Regular (Tipo 3)?")
        if self._is_regular(productions, steps):
            return self._build_result("Tipo 3", steps)

        steps.append("\nPaso 2: ¿La gramática es Libre de Contexto (Tipo 2)?")
        if self._is_context_free(productions, steps):
            return self._build_result("Tipo 2", steps)

        steps.append("\nPaso 3: ¿La gramática es Sensible al Contexto (Tipo 1)?")
        if self._is_context_sensitive(productions, steps):
            return self._build_result("Tipo 1", steps)

        # Si no cumple los criterios anteriores, es Tipo 0
        steps.append("\nPaso 4: La gramática es Recursivamente Enumerable (Tipo 0).")
        steps.append(
            "No cumple las restricciones de los tipos 3, 2 ni 1, "
            "por lo que se clasifica como Tipo 0 según la jerarquía de Chomsky."
        )
        return self._build_result("Tipo 0", steps)

    # ------------------------------------------------------------------
    # Verificaciones de tipo
    # ------------------------------------------------------------------
    def _symbol_classes(self, rhs):
        """
        Divide una cadena rhs en:
            - terminals: índices de símbolos terminales
            - nonterminals: índices de símbolos no terminales
        Convención:
            - No terminal = letra mayúscula (A-Z)
            - Terminal = cualquier otro símbolo visible
        """
        terminals = []
        nonterminals = []
        for i, ch in enumerate(rhs):
            if ch.isupper():
                nonterminals.append(i)
            else:
                terminals.append(i)
        return terminals, nonterminals

    def _is_regular(self, productions, steps):
        all_right_linear = True
        all_left_linear = True
        has_eps = False

        for lhs, rhs_list in productions.items():
            if len(lhs) != 1 or not lhs.isupper():
                steps.append(
                    f"  ❌ Lado izquierdo '{lhs}' no es un solo no terminal; "
                    "viola la forma regular."
                )
                return False

            for rhs in rhs_list:
                if rhs == "":
                    # ε-producción
                    has_eps = True
                    steps.append(f"  ⚠ {lhs} → ε (epsilon). Permitida solo si se maneja con cuidado.")
                    continue

                terminals, nonterminals = self._symbol_classes(rhs)

                if len(nonterminals) == 0:
                    # Solo terminales: OK
                    steps.append(f"  ✅ {lhs} → {rhs} (solo terminales, permitido en Tipo 3).")
                    continue

                if len(nonterminals) == 1:
                    nt_pos = nonterminals[0]
                    # Verificamos que todo lo demás sean terminales
                    if all(i in terminals or i == nt_pos for i in range(len(rhs))):
                        if nt_pos == len(rhs) - 1:
                            # ...A  (right-linear)
                            steps.append(f"  ✅ {lhs} → {rhs} (forma derecha lineal).")
                            all_left_linear = False
                            continue
                        if nt_pos == 0:
                            # A... (left-linear)
                            steps.append(f"  ✅ {lhs} → {rhs} (forma izquierda lineal).")
                            all_right_linear = False
                            continue

                # Si llega aquí, la producción no es regular
                steps.append(
                    f" {lhs} → {rhs} no cumple la forma lineal "
                    "(terminales + un solo no terminal en un extremo)."
                )
                return False

        # Si todas las producciones pasaron
        if has_eps:
            steps.append(
                " La gramática tiene producción(es) epsilon. "
                "En una teoría más estricta se requiere un tratamiento especial, "
                "pero aquí se acepta como Tipo 3 si el resto cumple."
            )
        steps.append("Todas las producciones cumplen la forma regular.")
        return True

    def _is_context_free(self, productions, steps):
        """
        Verifica si la gramática es Libre de Contexto (Tipo 2).
        Criterios:
        - Cada lado izquierdo es un solo no terminal (mayúscula).
        - El lado derecho puede ser cualquier cadena de terminales/no terminales (incluyendo ε).
        """
        for lhs, rhs_list in productions.items():
            if len(lhs) != 1 or not lhs.isupper():
                steps.append(
                    f" Lado izquierdo '{lhs}' no es un solo no terminal; "
                    "viola la definición de gramática libre de contexto."
                )
                return False

            for rhs in rhs_list:
                if rhs == "":
                    steps.append(f"  ✅ {lhs} → ε (epsilon permitido en Tipo 2).")
                else:
                    steps.append(f"  ✅ {lhs} → {rhs} es compatible con Tipo 2.")

        steps.append("✅ Todas las producciones cumplen las condiciones de Tipo 2.")
        return True

    def _is_context_sensitive(self, productions, steps):
        """
        Verifica si la gramática es Sensible al Contexto (Tipo 1).

        Criterios simplificados:
        - Ninguna producción reduce la longitud: |β| >= |α|.
        - Se permite S → ε solo si S no aparece en ningún lado derecho.
        """
        context_sensitive = True
        has_s_epsilon = False
        start_symbol = "S"

        # Verificar si S -> ε existe
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                if lhs == start_symbol and rhs == "":
                    has_s_epsilon = True

        # Verificar cada producción
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                alpha = lhs
                beta = rhs

                if has_s_epsilon and lhs == start_symbol and rhs == "":
                    # S → ε: permitido si S no aparece en RHS de ninguna producción
                    continue

                alpha_len = len(alpha)
                beta_len = len(beta)

                if beta_len < alpha_len:
                    steps.append(
                        f"  ❌ Producción {lhs} → {rhs if rhs != '' else 'ε'} "
                        f"reduce la longitud (|{alpha}|={alpha_len}, |{beta}|={beta_len})."
                    )
                    context_sensitive = False

        if has_s_epsilon:
            # verificar que S no aparezca en ningún lado derecho
            s_in_rhs = False
            for lhs, rhs_list in productions.items():
                for rhs in rhs_list:
                    if "S" in rhs:
                        s_in_rhs = True
                        break
                if s_in_rhs:
                    break
            if s_in_rhs:
                steps.append(
                    "  ❌ Se encontró S → ε pero S aparece en el lado derecho de alguna producción."
                )
                context_sensitive = False
            else:
                steps.append(
                    "  ✅ Producción S → ε permitida (S no aparece en ningún lado derecho)."
                )

        if context_sensitive:
            steps.append(
                "✅ Todas las producciones cumplen |β| ≥ |α| (condición simplificada de Tipo 1)."
            )
        return context_sensitive

    # ------------------------------------------------------------------
    # Clasificación de autómatas desde texto (muy sencilla)
    # ------------------------------------------------------------------
    def classify_automaton_from_text(self, text):
        """
        Clasificación de "autómatas" describiendo:
        - Si parece AFD/AFN → Tipo 3.
        - Si parece AP o Pila → Tipo 2.
        - Si menciona Cinta / Turing → Tipo 0.
        """
        steps = []
        steps.append("Análisis de autómata ingresado.")
        steps.append(f"Descripción original:\n{text}")

        lower = text.lower()

        if any(k in lower for k in ["pila", "pda", "pushdown", "autómata con pila"]):
            steps.append(
                "Se detectan referencias a autómatas con pila (PDA). "
                "Se asume un modelo equivalente a Tipo 2."
            )
            return self._build_result("Tipo 2", steps)

        if any(k in lower for k in ["turing", "cinta", "máquina de turing"]):
            steps.append(
                "Se detectan referencias a máquinas de Turing. "
                "Se clasifica como Tipo 0 por equivalencia de poder computacional."
            )
            return self._build_result("Tipo 0", steps)

        if any(k in lower for k in ["afd", "afn", "dfa", "nfa", "autómata finito"]):
            steps.append(
                "Se detectan referencias a autómatas finitos. "
                "Se asume que el lenguaje es regular (Tipo 3)."
            )
            return self._build_result("Tipo 3", steps)

        steps.append(
            "No se reconoció claramente el tipo de autómata; "
            "se asume el caso más general (Tipo 0)."
        )
        steps.append(
            "Clasificación basada en la relación clásica entre modelos de cómputo y la Jerarquía de Chomsky."
        )
        return self._build_result("Tipo 0", steps)

    def _build_result(self, grammar_type, steps):
        return {
            "type": grammar_type,
            "description": self.type_descriptions.get(
                grammar_type, "Clasificación desconocida"
            ),
            "explanation": "\n".join(steps),
            "steps": steps,
        }
