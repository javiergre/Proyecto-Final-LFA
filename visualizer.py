import graphviz
import os
from datetime import datetime


class GrammarVisualizer:
    def __init__(self):
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_diagram(self, productions, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"grammar_diagram_{timestamp}"

        dot = graphviz.Digraph(
            comment="Diagrama de gramática - Chomsky Classifier AI"
        )
        dot.attr(rankdir="LR", fontsize="10", fontname="Arial")

        # Nodo inicial
        if "S" in productions:
            dot.node("S", "S (inicio)", shape="doublecircle", style="filled", fillcolor="lightblue")

        # Crear nodos para variables
        for lhs in productions.keys():
            if lhs != "S":
                dot.node(lhs, lhs, shape="circle", style="filled", fillcolor="lightgray")

        # Crear aristas para producciones
        production_count = 0
        for lhs, rhs_list in productions.items():
            for rhs in rhs_list:
                production_count += 1
                rhs_str = "".join(rhs) if rhs else "ε"

                # Para producciones regulares A → aB, conectar A con B etiquetando con 'a'
                if len(rhs) == 2 and rhs[0].islower() and rhs[1].isupper():
                    dot.edge(lhs, rhs[1], label=rhs[0])
                else:
                    prod_node = f"prod_{production_count}"
                    dot.node(
                        prod_node,
                        f"{lhs} → {rhs_str}",
                        shape="rectangle",
                        style="filled",
                        fillcolor="lightyellow",
                        fontsize="9",
                    )
                    dot.edge(lhs, prod_node)

        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format="png", cleanup=True)
        return f"{output_path}.png"
    
    def generate_automaton_diagram_from_text(self, text, filename=None):
        import re
        from graphviz import Digraph

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"automaton_diagram_{timestamp}"

        dot = Digraph(comment="Automaton / Turing Machine")
        dot.attr(rankdir="LR", size="8,5")
        dot.attr("node", shape="circle", fontsize="12")

        # --- Estados ----------------------------------------------------
        states = set()
        initial_state = None
        accept_states = set()

        # Estados: {q0, q1, qaccept, qreject}
        m_states = re.search(r"Estados:\s*\{([^}]+)\}", text, re.IGNORECASE)
        if m_states:
            states = {s.strip() for s in m_states.group(1).split(",") if s.strip()}

        # Estado inicial: q0
        m_init = re.search(r"Estado\s+inicial:\s*([A-Za-z0-9_]+)", text, re.IGNORECASE)
        if m_init:
            initial_state = m_init.group(1).strip()
            states.add(initial_state)

        # Estado(s) de aceptación: qaccept  ó  {qaccept, qok}
        m_accept = re.search(
            r"Estado[s]?\s+de\s+aceptaci[óo]n:\s*\{?([^}\n]+)\}?",
            text,
            re.IGNORECASE,
        )
        if m_accept:
            for s in m_accept.group(1).split(","):
                st = s.strip()
                if st:
                    accept_states.add(st)
                    states.add(st)

        # --- Transiciones ----------------------------------------------
        trans_pattern = re.compile(
            r"δ\(\s*([A-Za-z0-9_]+)\s*,\s*([^)\n]+)\)\s*=\s*\(\s*([A-Za-z0-9_]+)\s*,\s*([^,]+)\s*,\s*([LR])\s*\)",
            re.UNICODE,
        )

        transitions = []
        for m in trans_pattern.finditer(text):
            q_from = m.group(1).strip()
            read_symbol = m.group(2).strip()
            q_to = m.group(3).strip()
            write_symbol = m.group(4).strip()
            direction = m.group(5).strip()

            states.add(q_from)
            states.add(q_to)

            label = f"{read_symbol}/{write_symbol},{direction}"
            transitions.append((q_from, q_to, label))

        # Crear nodos
        if not states:
            states = {"q0"}
            initial_state = initial_state or "q0"

        for s in states:
            if s in accept_states:
                dot.node(s, shape="doublecircle", style="filled", fillcolor="lightgreen")
            else:
                dot.node(s)

        # Flecha de inicio
        if initial_state:
            dot.node("__start__", shape="point")
            dot.edge("__start__", initial_state)

        # Aristas de transición
        for q_from, q_to, label in transitions:
            dot.edge(q_from, q_to, label=label)

        # Guardar diagrama
        output_path = os.path.join(self.output_dir, filename)
        dot.render(output_path, format="png", cleanup=True)
        return f"{output_path}.png"


    
    

